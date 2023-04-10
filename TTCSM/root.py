import arcpy


class root(object):
    """Handles instantiation of arcpy object and environmental settings"""

    def __init__(self, workspace=None, DEM=None):

        self.arcpy = arcpy
        self.arcpy.env.overwriteOutput = True
        self.arcpy.CheckOutExtension("spatial")

        self.workspace = workspace
        if self.workspace is not None:
            self.arcpy.env.workspace = workspace
        if DEM is not None:
            self.DEM = DEM
            self.arcpy.env.extent = self.DEM
            self.arcpy.env.cellSize = self.DEM
            self.arcpy.env.snapRaster = self.DEM
            self.arcpy.env.outputCoordinateSystem = self.DEM


if __name__ == '__main__':
    workspace = 'C:\\TEMP'
    DEM = 'C:\\TEST\\TTCSM_Frakes.gdb\\dem'
    a = root(workspace=workspace)
