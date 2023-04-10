import TTCSM.common as cmn
from TTCSM.root import root


class least_cost_path(root):
    """
        Creates a polyline feature with all of the least cost paths.

        One way cumulative travel times are calculated from the defined start
        point(s) and or start corridors(s) to all other locations within the
        area of interest.

        """

    def __init__(self,
                 startLocation,
                 destinations,
                 new_polyline_feature,
                 travelCost,
                 backlink,
                 workspace=None):
        super(least_cost_path, self).__init__(workspace=workspace)
        self.startLocation = startLocation
        self.travelCost = travelCost
        self.destinations = destinations
        self.backlink = backlink
        self.new_polyline_feature = new_polyline_feature

    def create(self):
        """
            Main method to create least cost path
            """
        self._least_cost_path_analysis()
        self._convert_to_poly()
        return self.outCostPathGrid

    def _least_cost_path_analysis(self):
        self.outCostPathGrid = self.arcpy.sa.CostPath(
            in_destination_data=self.destinations
            , in_cost_distance_raster=self.travelCost
            , in_cost_backlink_raster=self.backlink)

    def _convert_to_poly(self):
        self.arcpy.RasterToPolyline_conversion(
            self.outCostPathGrid
            , self.new_polyline_feature
            , "NODATA", "0"
            , "NO_SIMPLIFY"
            , "VALUE")


if __name__ == '__main__':
    startLocation = 'C:\\CODE\\CostSurface\\TestingData\\starting_pts.shp'
    travelCost = 'C:\\CODE\\CostSurface\\scratch\\travel_speed_surface_spM.tif'
    workspace = 'C:\\CODE\\CostSurface\\scratch'
    destinations = 'C:\\CODE\\CostSurface\\TestingData\\destinations.shp'
    backlink = r'C:\CODE\CostSurface\scratch\backlink.tif'
    new_polyline_feature = r'C:\CODE\CostSurface\scratch\least_cost_paths.shp'

    lcp = least_cost_path(
        startLocation=startLocation,
        new_polyline_feature=new_polyline_feature,
        travelCost=travelCost,
        destinations=destinations,
        backlink=backlink,
        workspace=workspace)
    results = lcp.create()
    results.save(workspace + '\\least_cost_path.tif')
