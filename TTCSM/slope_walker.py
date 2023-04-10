from TTCSM.root import root

from TTCSM.digital_elevation_model import digital_elevation_model as d


class slope_walker(root):
    """
    Calculates walking speed in seconds per meter based on the slope derived from a DEM

    Arguments:
        DEM - The gridded digital elevation model
        walking_speed_mph - The normal walking speed on a flat surface.  Walking
            rates up and down hill will be a fraction of this value
        workspace (optional) - The scratch workspace where temporary files are written
        max_slope_cap = None (optional) - If specified, any slope above this value will be capped to that value.
            For example, if a max slope cap value of 20 is specified, any slope calcualated
            above 20 will be set at 20 degrees.

    """

    def __init__(self
                 , DEM
                 , walking_speed_mph=3.1
                 , workspace=None
                 , max_slope_cap=None):
        super(slope_walker, self).__init__(workspace=workspace, DEM=DEM)
        self.DEM = DEM
        self.walking_speed_mph = float(walking_speed_mph)
        self.walking_speed_adjustment_ratio = self.walking_speed_mph / 3.13
        self.max_slope_cap = max_slope_cap

    def create(self):
        self._calc_slope()
        self._calc_walking_speed()
        self._convert_travel_speed_to_SecM()
        return self.slope_walk

    def _calc_slope(self):
        '''calculate slope of DEM'''
        dem = d(self.DEM)
        self.slope_surface = dem.get_degree_slope(max_slope_cap=self.max_slope_cap)

    def _cap_slope(self):
        self.slope_surface = dem.cap_slope()

    def _calc_walking_speed(self):
        """Derive Travel Speed from slope (Kilometers per hour)...Note Tan is in radians"""
        self.slope_speed_kmH = (6 * self.arcpy.sa.Exp(
            -3.5 * (self.arcpy.sa.Abs(self.arcpy.sa.Tan((self.slope_surface) / (57.29578)) + .05))))

    def _convert_travel_speed_to_SecM(self):
        """ Convert Travel Speed to Seconds per Meter..."""
        algTSP2 = (1 / (self.slope_speed_kmH / 3.6))
        self.slope_walk = (algTSP2 / self.walking_speed_adjustment_ratio)


if __name__ == '__main__':
    DEM = 'C:\\CODE\\CostSurface\\old\\TestingData\\DEM.tif'
    workspace = 'C:\\CODE\\CostSurface\\scratch'
    walking_speed_mph = 3.1
    sw = slope_walker(DEM=DEM, walking_speed_mph=walking_speed_mph, workspace=workspace)
    print(sw.create())
