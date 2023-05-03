import TTCSM.common as cmn
from TTCSM.cost_distance import cost_distance


class path_distance(cost_distance):
    """
        Calculates the path distance as defined here:
            http://resources.arcgis.com/en/help/main/10.1/index.html#//009z0000001q000000

        Returns
        Cumulative travel time in seconds

        """

    def __init__(self
                 , startLocation
                 , travelCost
                 , DEM
                 , out_backlink_raster=None
                 , highCutAngle=40
                 , verticalGraphType=None
                 , zeroFactor=1
                 , verticalGraphTable=None
                 , timeCap=28800
                 , workspace=None):
        super(path_distance, self).__init__(startLocation=startLocation,
                                            travelCost=travelCost, DEM=DEM, timeCap=timeCap,
                                            workspace=workspace, out_backlink_raster=out_backlink_raster)

        self.verticalGraphType = verticalGraphType.lower()
        self.zeroFactor = zeroFactor
        self.verticalGraphTable = verticalGraphTable
        self.highCutAngle = highCutAngle
        self.lowCutAngle = self.highCutAngle * -1

        self._set_vertical_factor()

    def _set_vertical_factor(self):
        """Do all of the initialization of the vertical factor information"""
        self.pathDistanceTypes = {'binary': self.arcpy.sa.VfBinary,
                                  'linear': self.arcpy.sa.VfLinear,
                                  'symmetrical linear ': self.arcpy.sa.VfSymLinear,
                                  'inverse linear': self.arcpy.sa.VfInverseLinear,
                                  'symmetrical inverse linear': self.arcpy.sa.VfSymInverseLinear}

        self.pathDistanceTypes_Trig = {'cosine': self.arcpy.sa.VfCos,
                                       'secant': self.arcpy.sa.VfSec,
                                       'cosine-secant': self.arcpy.sa.VfCosSec,
                                       'secant-cosine': self.arcpy.sa.VfSecCos}

        if self.verticalGraphType in list(self.pathDistanceTypes.keys()):
            self.verticalFactor = self.pathDistanceTypes[self.verticalGraphType](
                zeroFactor=self.zeroFactor
                , lowCutAngle=self.lowCutAngle
                , highCutAngle=self.highCutAngle)

        elif self.verticalGraphType in list(self.pathDistanceTypes_Trig.keys()):
            self.verticalFactor = self.pathDistanceTypes_Trig[self.verticalGraphType](-90, 90, 1)

        elif self.verticalGraphTable is not None:  # user defined vertical factor graph
            self.verticalFactor = VfTable(self.verticalGraphTable)

        else:
            cmn.quit('Undefined path distance. Terminating')

    def _calc_distance(self):

        self.outCD = self.arcpy.sa.PathDistance(
            in_source_data=self.startLocation
            , in_cost_raster=self.travelCost
            , in_surface_raster=self.DEM
            , in_vertical_raster=self.DEM
            , vertical_factor=self.verticalFactor
            , maximum_distance=self.timeCap
            , out_backlink_raster=self.out_backlink_raster)


if __name__ == '__main__':
    folder = r'C:\CODE\CostSurface\TestingData'
    startLocation = folder + r'\starting_pts.shp'
    DEM = folder + r'\dem'
    verticalGraphType = 'Binary'
    zeroFactor = 1
    verticalGraphTable = None
    timeCap = 28800
    travelCost = 'C:\\CODE\\CostSurface\\scratch\\travel_speed_surface_spM.tif'
    workspace = 'C:\\CODE\\CostSurface\\scratch'
    highCutAngle = 40

    pd = path_distance(startLocation=startLocation,
                       travelCost=travelCost,
                       DEM=DEM,
                       workspace=workspace,
                       verticalGraphType=verticalGraphType,
                       zeroFactor=zeroFactor,
                       verticalGraphTable=verticalGraphTable,
                       timeCap=timeCap
                       )

    cd = pd.create()
    cd.save('C:\\CODE\\CostSurface\\scratch\\cost_distance_ByPath.tif')
