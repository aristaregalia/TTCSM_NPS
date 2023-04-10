from TTCSM.root import root

from TTCSM.feature_stacker import feature_stacker
from TTCSM.unit_converter import unit_converter as uc


class network_speed_surface(root):
    """
    Generates a network speed surface grid which has
    calculated speed (seconds/per meter) across the extent of the input DEM.
    Cells coincident with the network(s) have speed defined by the
    network speed (which is defined in miles per hour
     and then converted to seconds per meter).

    Network layers should be listed in order of priority, with the preferred mode
    of travel listed first.

    CREATES
     Creates grid feature that defines the time of movement within each cell
     (seconds per meter -  Sec/M)
    """

    def __init__(self, network_layers, DEM, workspace=None):
        super(network_speed_surface, self).__init__(workspace=workspace, DEM=DEM)
        self.network_layers = network_layers
        self.DEM = DEM

    def create(self):
        self._add_priority_field()
        self._stack_layers()
        self._convert_mpH_to_secM()
        return self.new_surface

    def _stack_layers(self):
        self.nss = feature_stacker(self.network_layers, self.DEM, self.workspace)
        self.stacked_layers = self.nss.create()

    def _convert_mpH_to_secM(self):
        '''
        Converts from miles/per hour to seconds/per meter
        '''
        #c = uc.unit_converter(self.stacked_layers)
        c = uc(self.stacked_layers)
        self.new_surface = c.milesHour_to_secondsMeter()

    def _add_priority_field(self):
        '''
        Adds priority field to be used in feature stacker conversion of vector to raster
        '''
        for line in self.network_layers:
            self.arcpy.AddField_management(line[0], 'PRIORITY', 'LONG')
            self.arcpy.CalculateField_management(line[0], 'PRIORITY', '!' + line[1] + '!', 'PYTHON_9.3')


if __name__ == '__main__':
    from TTCSM.unit_converter import unit_converter as uc2

    network_layers = [('C:\CODE\CostSurface\TestingData\Roads.shp', 'Speed_mph')]
    DEM = 'C:\\CODE\\CostSurface\\TestingData\\DEM_feet'
    # DEM = 'C:\\CODE\\CostSurface\\TestingData\\DEM'
    workspace = 'C:\\CODE\\CostSurface\\scratch'
    cs = network_speed_surface(
        network_layers=network_layers
        , DEM=DEM
        , workspace=workspace)
    netSpeed = cs.create()
    netSpeed.save('C:\\TEMP\\networkSpeed')
    c = uc2(netSpeed)
    mph = c.secondsMeter_to_milesHour()
    mph.save('C:\\CODE\\CostSurface\\scratch\\network_mph.img')
