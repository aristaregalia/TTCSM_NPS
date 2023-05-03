import os

import arcpy as arcpy0
import TTCSM.TTCSM_GUI as gui

def _debug(fileLocation, message=None):
    """
    Optional debugger to write arguments to a specified file and folder location
    """
    try:
        outfile = open(fileLocation, 'w')
        outfile.write(str(message))
        outfile.close()
    except:
        pass


args = {}

x = 0
while True:
    try:
        args['arg' + str(x)] = str(arcpy0.GetParameterAsText(x))
        x += 1
    except:
        break
fileLocation = os.path.dirname(args['arg0']) + 'debug.txt'
fileLocation = 'C:\\TEMPY\\debug.txt'
_debug(fileLocation, args)
gui.process_request(args)
