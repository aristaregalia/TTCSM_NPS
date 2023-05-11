from TTCSM.slope_walker import slope_walker
from TTCSM.digital_elevation_model import digital_elevation_model as dm
from TTCSM.feature_stacker import feature_stacker as fs
from TTCSM.network_speed_surface import network_speed_surface


class base_speed_surface(network_speed_surface):
    """
        STEPS:

        RETURNS
        travel_speed_surface_sM - Travel speed in seconds per meter over all base
        layers

        """

    def __init__(self
                 , base_layers
                 , DEM
                 , walking_speed_mph=3.1
                 , workspace=None
                 , max_slope_cap=None):
        super(base_speed_surface, self).__init__(base_layers, DEM, workspace)
        self.walking_speed_mph = walking_speed_mph
        self.max_slope_cap = max_slope_cap
        self.base_layers = base_layers

    def create(self):
        self._add_priority_field()
        self._stack_layers()
        self._calc_slope_walking_speed()
        self._calc_resistance()
        self._set_zero_to_Null()
        return self.new_surface

    def _calc_slope_walking_speed(self):
        sw =slope_walker(
            DEM=self.DEM
            , walking_speed_mph=self.walking_speed_mph
            , workspace=self.workspace
            , max_slope_cap=self.max_slope_cap)
        self.slope_walk_speed = sw.create()

    def _calc_resistance(self):
        """
            Divide the walking speed by the resitsance.
            If the resistance is zero, set walking speed to zero.
            """
        self.new_surface = self.slope_walk_speed / self.stacked_layers

    def _set_zero_to_Null(self):
        hasData = self.arcpy.sa.GreaterThan(self.new_surface, 0)
        self.new_surface = self.arcpy.sa.SetNull(hasData != 1, self.new_surface)

    def _add_priority_field(self):
        """
            Adds priority field to be used in feature stacker conversion of vector to raster
            """
        for line in self.base_layers:
            try:
                if self.arcpy.Describe(line[0]).shapeType == 'Polyline':
                    self.arcpy.AddField_management(line[0], 'PRIORITY', 'FLOAT')
                    self.arcpy.CalculateField_management(line[0], 'PRIORITY', '1.0/!' + line[1] + '!', 'PYTHON_9.3')
            except:
                pass


if __name__ == '__main__':
    from TTCSM.unit_converter import unit_converter as uc

    base_layers = [
        (r'C:\CODE\CostSurface\TestingData\Streams.shp', 'Cost_perc'),
        (r'C:\CODE\CostSurface\TestingData\Lakes.shp', 'Cost_perc'),
        (r'C:\CODE\CostSurface\TestingData\Landcover.shp', 'Cost_perc')]

    DEM = 'C:\\CODE\\CostSurface\\TestingData\\DEM.tif'
    workspace = 'C:\\TEMP'
    walking_speed_mph = 10

    tss = base_speed_surface(
        base_layers=base_layers,
        DEM=DEM,
        workspace=workspace
        , walking_speed_mph=walking_speed_mph)

    a = tss.create()
    c = uc.unit_converter(a)
    mph = c.secondsMeter_to_milesHour()
    mph.save('C:\\TEMP\\mph.tif')
