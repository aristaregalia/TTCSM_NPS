from TTCSM.travel_speed_surface import travel_speed_surface
from TTCSM.cost_distance import cost_distance
import TTCSM.common as cmn
from TTCSM.unit_converter import unit_converter as uc
from TTCSM.digital_elevation_model import digital_elevation_model
from TTCSM.path_distance import path_distance
from TTCSM.least_cost_path import least_cost_path
from TTCSM.root import root


class TTCSM(object):
    """
    Class that creates a travel time cost surface grid based on one or more
    features. See associated Help Manual which further describes the model logic.


    REQUIRED ARGUMENTS
    workspace - scratch workspace to save temporary files
    DEM - Raster digital elevation model
    startLocation - Feature or raster defining one or more start location(s)


    OPTIONAL ARGUMENTS
    network_layers - one or more motorized network layers representing assisted
        travel (e.g., cars)
    trail_layers -
    base_layers -
    maximum_slope (default = 31 degrees) - The slope of the surface
        a person can walk on before the slope becomes an absolute barrier
    walking_speed_mph (default = 3.1 mph) - The average walking speed of a person
        on a flat, smooth surface
    timeCap (default = 3600 seconds) - The maximim travel time before the analysis
        is stopped

    destinations -
    out_cost_distance_file -
    new_polyline_feature -


    RETURNS
    Grid of travel cost in seconds

    EXAMPLE

    sourceData = 'D:\\CostSurface\\TestingData\\'

    workspace = 'D:\\CostSurface\\scratch'
    DEM = sourceData + 'dem'
    startLocation = sourceData + 'Starting_Points.shp'


    out_cost_distance_file = workspace + '\\cost_distance.img'



    base_layers =  [
        (sourceData + 'Streams.shp', 'PMTS'),
        (sourceData + 'Landcover.shp', 'PMTS')]
    network_layers =  [(sourceData + 'Roads.shp', 'Speed_mph')]
    trail_layers =  [(sourceData + 'Trails.shp', 'PMTS')]
    maximum_slope = 31

    walking_speed_mph = 3.1


    timeCap = 3600

    destinations = sourceData + 'destinations.shp'

    new_polyline_feature = workspace + '\\least_cost_path.shp'


    #INSTANTIATE
    t = TTCSM(
        workspace = workspace
        ,DEM = DEM
        ,startLocation = startLocation
        ,network_layers = network_layers
        ,trail_layers = trail_layers
        ,base_layers = base_layers
        ,out_cost_distance_file = out_cost_distance_file
        ,new_polyline_feature = new_polyline_feature
        ,maximum_slope = maximum_slope
        ,walking_speed_mph = walking_speed_mph
        ,timeCap = timeCap
        ,destinations = destinations
        )

    #TEST COST DISTANCE
    cd = t.create()
    cd.save(workspace + '\\cost_distance.tif')


    #TEST BINARY PATH DISTANCE
    verticalGraphType= 'binary'
    t.verticalGraphType = verticalGraphType
    cd = t.create()
    cd.save(workspace + '\\cost_distance_binary.tif')


    """

    def __init__(self
                 , workspace
                 , DEM
                 , startLocation
                 , out_cost_distance_file
                 , base_layers=None
                 , trail_layers=None
                 , network_layers=None
                 , maximum_slope=31
                 , walking_speed_mph=3.1
                 , timeCap=28800
                 , verticalGraphType=None
                 , destinations=None,
                 new_polyline_feature=None):

        # required arguments
        self.workspace = workspace  # workspace for all of the processing
        self.startLocation = startLocation  # Start location(s) point data for cost or path distance calculation
        self.network_layers = network_layers
        self.trail_layers = trail_layers  # Trail Network
        self.DEM = DEM  # Digital Elevation Model
        self.out_cost_distance_file = out_cost_distance_file

        # optional arguments
        self.base_layers = base_layers  ## List of features that define the cost of unassisted travel (i.e., walking)
        self.walking_speed_mph = float(
            walking_speed_mph)  ## Average walking speed for the scenario when walking a smooth flat surface (Miles/Hr)
        self.maximum_slope = float(maximum_slope)  ## Value in degrees defined as being to steep for travel
        self.timeCap = float(
            timeCap)  ## Maximum cost distance travel time calculated in seconds (28800/3600 = 8 hours).
        self.verticalGraphType = verticalGraphType  ## Select one of the following vertical factor graph (weights)to be used in path distance modeling: ("Binary" | "Linear" | "Sym_linear" | "Inverse_Linear" | "Sym_Inverse_Linear" | "Cos" | "Sec" | "Cos_Sec" | "Sec_Cos" | "Table").  See documentation for further definition.
        self.destinations = destinations
        self.new_polyline_feature = new_polyline_feature
        if '.gdb' in self.workspace:
            self.out_backlink_raster = self.workspace + '\\out_backlink'
        else:
            self.out_backlink_raster = self.workspace + '\\out_backlink.img'

    def create(self):
        self._create_travel_speed_surface_layer()
        self._create_cost_distance_layer()
        self._create_least_cost_path()
        return self.cost_distance

    def _create_travel_speed_surface_layer(self):
      #  tcs = travel_speed_surface.travel_speed_surface(
      tcs = travel_speed_surface(
            base_layers=self.base_layers,
            network_layers=self.network_layers,
            trail_layers=self.trail_layers,
            maximum_slope=self.maximum_slope,
            DEM=self.DEM,
            workspace=self.workspace,
            walking_speed_mph=self.walking_speed_mph)
      self.travelSpeed = tcs.create()

    def _create_cost_distance_layer(self):
        if self.verticalGraphType is None:
            self._cost_distance()
        else:
            self._path_distance()
        self.cost_distance.save(self.out_cost_distance_file)

    def _cost_distance(self):
        cdl = cost_distance.cost_distance(
            startLocation=self.startLocation,
            travelCost=self.travelSpeed,
            DEM=self.DEM,
            workspace=self.workspace,
            timeCap=self.timeCap,
            out_backlink_raster=self.out_backlink_raster)

        self.cost_distance = cdl.create()

    def _path_distance(self):
        pd = path_distance(
            startLocation=self.startLocation,
            travelCost=self.travelSpeed,
            DEM=self.DEM,
            workspace=self.workspace,
            verticalGraphType=self.verticalGraphType,
            zeroFactor=1,
            verticalGraphTable=None,
            timeCap=self.timeCap,
            out_backlink_raster=self.out_backlink_raster)
        self.cost_distance = pd.create()

    def _create_least_cost_path(self):
        if self.destinations is not None and self.new_polyline_feature is not None:
            #lcp = least_cost_path.least_cost_path(
             lcp=least_cost_path(
                startLocation=self.startLocation,
                new_polyline_feature=self.new_polyline_feature,
                travelCost=self.cost_distance,
                destinations=self.destinations,
                backlink=self.out_backlink_raster,
                workspace=self.workspace)
             results = lcp.create()


if __name__ == '__main__':
    workspace = 'C:\\TEMP\\'
    base = 'C:\\CODE\\CostSurface\\TestingData\\'
    base_layers = [
        (base + 'Streams.shp', 'PMTS'),
        (base + 'Landcover.shp', 'PMTS')]
    network_layers = [(base + 'Roads.shp', 'Speed_mph')]
    trail_layers = [(base + 'Trails.shp', 'PMTS')]
    maximum_slope = 3
    DEM = base + 'dem'
    walking_speed_mph = 3

    startLocation = base + 'Starting_Points.shp'
    timeCap = 3600

    destinations = base + 'destinations.shp'
    out_cost_distance_file = workspace + 'cost_distance.img'
    new_polyline_feature = workspace + 'least_cost_path.shp'

    # INSTANTIATE
    t = TTCSM(
        workspace=workspace
        , DEM=DEM
        , startLocation=startLocation
        , network_layers=network_layers
        , trail_layers=trail_layers
        , base_layers=base_layers
        , out_cost_distance_file=out_cost_distance_file
        , new_polyline_feature=new_polyline_feature
        , maximum_slope=maximum_slope
        , walking_speed_mph=walking_speed_mph
        , timeCap=timeCap
        # ,destinations = destinations
    )

    # TEST COST DISTANCE
    cd = t.create()
    cd.save(workspace + 'cost_distance.tif')

    # TEST BINARY PATH DISTANCE
##    verticalGraphType= 'binary'
##    t.verticalGraphType = verticalGraphType
##    cd = t.create()
##    cd.save(workspace + '\\cost_distance_binary.tif')
