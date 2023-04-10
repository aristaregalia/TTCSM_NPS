import os

from TTCSM.base_speed_surface import base_speed_surface


class trail_speed_surface(base_speed_surface):
    """
    Cells coincident with the trail network have a
    speed defined by the trail slope (which is diffent than the DEM slope)
    and the resistance of the trail itself
    (e.g., rough vs smooth trail).

    RETURNS
    Walking speed along trail in seconds/per meter

    """

    def __init__(self, trail_layers, DEM, walking_speed_mph=2.5, workspace=None, max_slope_cap=None):
        super(trail_speed_surface, self).__init__(trail_layers, DEM, walking_speed_mph, workspace, max_slope_cap)
        self.trail_layers = trail_layers

    def create(self):
        """
        Main method with call each of the hidden methods to create the trail
            speed surface
        RETURNS:
            File path to the new grid created
        """
        self._add_priority_field()
        self._stack_layers()
        self._set_trail_elevation_as_DEM()
        self._calc_slope_walking_speed()
        self._calc_resistance()
        return self.new_surface

    def _set_trail_elevation_as_DEM(self):
        """
        DEM must be projected coordinates system
        and have the same units (e.g., all in meters)

        Reclassify trails to a value of 1 and then assign DEM elevation to
        each trail cell (Trail X DEM)
        """
        self.reclass = self.arcpy.sa.Reclassify(self.stacked_layers, "VALUE", "0 100000 1", "DATA")
        self.DEM = (self.reclass * self.arcpy.sa.Raster(self.DEM))

    def _add_priority_field(self):
        """
        Adds priority field to be used in feature stacker conversion of vector to raster
        """
        for line in self.base_layers:
            self.arcpy.AddField_management(line[0], 'PRIORITY', 'FLOAT')
            self.arcpy.CalculateField_management(line[0], 'PRIORITY', '!' + line[1] + '!', 'PYTHON_9.3')


if __name__ == '__main__':
    from TTCSM.unit_converter import unit_converter as uc

    base = 'C:\\CODE\\CostSurface\\TestingData\\'
    workspace = 'C:\\TEMP'
    trail_layers = [(base + '\\Trails.shp', 'PMTS')]
    DEM = base + '\\dem'
    walking_speed_mph = 10

    tss = trail_speed_surface(
        DEM=DEM
        , trail_layers=trail_layers
        , walking_speed_mph=walking_speed_mph
        , workspace=workspace)
    trailSpd = tss.create()
    trailSpd.save(workspace + '\\trail_speed_surface.tif')

    # CHECK FOR PROPER SPEED
    c = uc(trailSpd)
    mph = c.secondsMeter_to_milesHour()
    mph.save(workspace + '\\trailSpd_mph.tif')
