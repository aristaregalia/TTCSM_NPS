import TTCSM.common as cmn
from TTCSM.root import root


class cost_distance(root):
    """
        Travel time output grids are given in seconds

        """

    def __init__(self,
                 startLocation,
                 travelCost,
                 DEM,
                 out_backlink_raster=None,
                 timeCap=28800,
                 workspace=None):
        super(cost_distance, self).__init__(workspace=workspace, DEM=DEM)

        self.startLocation = startLocation
        self.travelCost = travelCost
        self.timeCap = int(timeCap)
        self.out_backlink_raster = out_backlink_raster

    def create(self):
        """
            Main method to create the cost distance layer
            """
        self._calc_distance()
        self._convert_travel_time()
        return self.outCD

    def _calc_distance(self):
        self.outCD = self.arcpy.sa.CostDistance(
            in_source_data=self.startLocation
            , in_cost_raster=self.travelCost
            , maximum_distance=self.timeCap
            , out_backlink_raster=self.out_backlink_raster)

    def _convert_travel_time(self):
        """
            creates respective grids in hours, minutes and seconds and
            converts all times to integers
            """
        pass


if __name__ == '__main__':
    base = 'D:\\BRENT\\CODE\\CostSurface\\TestingData\\'
    startLocation = base + 'starting_pts.shp'
    travelCost = 'D:\\BRENT\\CODE\\CostSurface\\scratch\\travel_speed_surface_secM.img'
    DEM = base + 'dem'
    timeCap = 28800
    workspace = 'D:\\BRENT\\CODE\\CostSurface\\scratch'
    out_backlink_raster = 'D:\\BRENT\\CODE\\CostSurface\\scratch\\backlink.tif'

    cd = cost_distance(startLocation=startLocation,
                       travelCost=travelCost,
                       DEM=DEM,
                       timeCap=timeCap,
                       out_backlink_raster=out_backlink_raster,
                       workspace=workspace
                       )
    f = cd.create()
    f.save('D:\\BRENT\\CODE\\CostSurface\\scratch\\cost_surface.tif')
