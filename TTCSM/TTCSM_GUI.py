from TTCSM import TTCSM_INFO
from TTCSM.TTCSM_INFO import TTCSM


def set_none(value):
    if value == '':
        return None
    else:
        return value


def process_request(args):
    workspace = args['arg0'] + '\\'
    startLocation = args['arg1']
    DEM = args['arg2']
    out_cost_distance_file = args['arg3']
    walking_speed_mph = float(args['arg4'])
    maximum_slope = float(args['arg5'])
    max_travel_time_sec = int(args['arg6'])
    roadsData = args['arg7']
    road_speed_field = args['arg8']
    trailsData = args['arg9']
    trails_field = args['arg10']
    streams = set_none(args['arg11'])
    streams_field = args['arg12']
    lakes = set_none(args['arg13'])
    lakes_field = args['arg14']
    landcover = set_none(args['arg15'])
    landcover_field = args['arg16']
    verticalGraphType = set_none(args['arg17'])
    destinations = set_none(args['arg18'])
    new_polyline_feature = set_none(args['arg19'])

    base_layers = []
    if streams is not None: base_layers.append((streams, streams_field))
    if lakes is not None: base_layers.append((lakes, lakes_field))
    if landcover is not None: base_layers.append((landcover, landcover_field))
    if len(base_layers) == 0:
        base_layers = None

    network_layers = []
    if roadsData != '': network_layers.append((roadsData, road_speed_field))
    if len(network_layers) == 0:
        network_layers = None

    trail_layers = []
    if trailsData != '': trail_layers.append((trailsData, trails_field))
    if len(trail_layers) == 0:
        trail_layers = None

    t = TTCSM(workspace=workspace
              , DEM=DEM
              , network_layers=network_layers
              , trail_layers=trail_layers
              , startLocation=startLocation
              , base_layers=base_layers
              , walking_speed_mph=walking_speed_mph
              , maximum_slope=maximum_slope
              , verticalGraphType=verticalGraphType
              , out_cost_distance_file=out_cost_distance_file
              , destinations=destinations
              , new_polyline_feature=new_polyline_feature
              , timeCap=max_travel_time_sec
              )
    t.create()


if __name__ == '__main__':
    # args = {'arg8': '-Select Field-', 'arg9': 'C:\\TEST\\TTCSM_Frakes.gdb\\Trail', 'arg0': 'C:\\TEST\\workspace', 'arg1': 'C:\\TEST\\TTCSM_Frakes.gdb\\Points\\Start_Point', 'arg2': 'C:\\TEST\\TTCSM_Frakes.gdb\\dem', 'arg3': 'C:\\TEST\\workspace\\newCF2.tif', 'arg4': '3.1', 'arg5': '31', 'arg6': '28800', 'arg7': '', 'arg12': '-Select Field-', 'arg13': '', 'arg10': 'Speed_Travel', 'arg11': '', 'arg16': '-Select-', 'arg17': '', 'arg14': '-Select Field-', 'arg15': '', 'arg18': '', 'arg19': ''}
    # args = {'arg8': '-Select Field-', 'arg9': 'C:\\TEST\\TTCSM_Frakes.gdb\\Trail', 'arg0': 'C:\\TEMP', 'arg1': 'C:\\TEST\\TTCSM_Frakes.gdb\\Points\\Start_Point', 'arg2': 'C:\\TEST\\TTCSM_Frakes.gdb\\DEM', 'arg3': 'C:\\TEMP\\cs.tif', 'arg4': '3.1', 'arg5': '31', 'arg6': '28800', 'arg7': '', 'arg12': '-Select Field-', 'arg13': '', 'arg10': 'Speed_Travel', 'arg11': '', 'arg16': 'Speed', 'arg17': '', 'arg14': '-Select Field-', 'arg15': 'C:\\TEST\\TTCSM_Frakes.gdb\\LandCover', 'arg18': '', 'arg19': ''}
    # process_request(args)
    #
    # args = {'arg8': 'Speed_mph', 'arg9': 'C:\\TestingData\\TestingData\\Trails.shp',
    #         'arg0': 'C:\\TestingData\\workspace',
    #         'arg1': 'C:\\TestingData\\TestingData\\Starting_Points.shp', 'arg2': 'C:\\TestingData\\TestingData\\dem',
    #         'arg3': 'C:\\TestingData\\workspace\\TTCSM_OUTPUT.gdb\\CostSurfPMTS0new3', 'arg4': '3.1', 'arg5': '31',
    #         'arg6': '28800', 'arg7': 'C:\\TestingData\\TestingData\\Roads.shp',
    #         'arg12': 'PMTS', 'arg13': 'C:\\PROJECTS\\TTCSM_NEW_test\\TTCSM_NEW_test.gdb\\Lakes_test_1', 'arg10': 'PMTS', 'arg11': 'C:\\TestingData\\TestingData\\Streams.shp', 'arg16': 'PMTS', 'arg17': 'Linear',
    #         'arg14': 'PMTS', 'arg15': 'C:\\TestingData\\TestingData\\Landcover.shp',
    #         'arg18': 'C:\\TestingData\\TestingData\\Destinations.shp',
    #         'arg19': 'C:\\TestingData\\workspace\\TTCSM_OUTPUT.gdb\\CostPMTS0new3'}

    args = {'arg0': 'C:\\ROMN\GIS\\TTCSM\\Python3Arista\\workspace',
            'arg1': 'C:\\ROMN\\GIS\\TTCSM\\Python3Arista\\TestingData\\Starting_Points.shp',
            'arg2': 'C:\\ROMN\\GIS\\TTCSM\\Python3Arista\\TestingData\\dem',
            'arg3': 'C:\\ROMN\\GIS\\TTCSM\\Python3Arista\\Python3Arista.gdb\\CS_Linear_Lakes_Dest4_Python3',
            'arg4': '3.1',
            'arg5': '31',
            'arg6': '28800',
            'arg7': 'C:\\ROMN\\GIS\\TTCSM\\Python3Arista\\TestingData\\Roads.shp',
            'arg8': 'Speed_mph',
            'arg9': 'C:\\ROMN\\GIS\\TTCSM\\Python3Arista\\TestingData\\Trails.shp',
            'arg10': 'PMTS',
            'arg11': 'C:\\ROMN\\GIS\\TTCSM\\Python3Arista\\TestingData\\Streams.shp',
            'arg12': 'PMTS',
            'arg13': 'C:\\ROMN\\GIS\\TTCSM\\Python3Arista\\Python3Arista.gdb\\LakesPython3Arista',
            'arg14': 'PMTS',
            'arg15': 'C:\\ROMN\\GIS\\TTCSM\\Python3Arista\\TestingData\\Landcover.shp',
            'arg16': 'PMTS',
            'arg17': 'Linear',
            'arg18': 'C:\\ROMN\\GIS\\TTCSM\\Python3Arista\\TestingData\\Destinations.shp',
            'arg19': 'C:\\ROMN\\GIS\\TTCSM\\Python3Arista\\Python3Arista.gdb\\CS_Linear_Lakes_Dest4_Python3_Script'}


    process_request(args)
