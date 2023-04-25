import os

from TTCSM.root import root


class feature_stacker(root):
    """
    For a given set of features (raster or vector):
        1. Converts them to raster with the same cell size and extent
        2. Stacks them in order (with last in list being on the bottom)

    Feature_List must be a set of feature/attribute pairs used to convert to raster:
        feature_list =  [('C:\CODE\CostSurface\TestingData\Roads.shp', 'Speed')]


    CREATES
     Single grid representing the stacked features
    """

    def __init__(self, feature_list, DEM, workspace=None):
        super(feature_stacker, self).__init__(workspace=workspace, DEM=DEM)
        self.feature_list = feature_list
        self.gridded_layers = []
        self.workspace = workspace

    def create(self):
        """
        Main method to stack the layers
        """
        self._get_raster_extension()
        self._rasterize_layers()
        self._set_base_layer(self.gridded_layers.pop(0))
        for count, layer in enumerate(self.gridded_layers):
            self._add_cost_overlay(layer)
        return self.base_layer

    def _set_base_layer(self, base_layer):
        self.base_layer = base_layer

    def _add_cost_overlay(self, layer):
        """
        Add each respective layer to the base_speed_surface
        where the layer is not Null
        """
        layerIsNull = self.arcpy.sa.IsNull(layer)
        self.base_layer = self.arcpy.sa.Con(layerIsNull, self.base_layer, layer)

    def _rasterize_layers(self):
        """
        Convert all layers to raster format (if needed).
        Reverse order of grids so the first grid to be processed is the base layer
        """
        for line in self.feature_list:
            if isinstance(line[0], self.arcpy.Raster):
                featureName = line[0]
            else:
                try:
                    featureName = self.arcpy.Raster(featureName)

                    featureNameNoFail = os.path.basename(line[0]).split('.')[0] + self.ras_ext  #KRS Added 4/25/2023
                    self.arcpy.conversion.PolygonToRaster(line[0], line[1], featureNameNoFail, 'MAXIMUM_COMBINED_AREA',
                                                          '', self.DEM)  #KRS Added 4/25/2023
                except:
                    featureName = os.path.basename(line[0]).split('.')[0] + self.ras_ext
                    if self.arcpy.Describe(line[0]).shapeType == 'Polyline':
                        self.arcpy.PolylineToRaster_conversion(line[0], line[1], featureName, 'MAXIMUM_COMBINED_LENGTH',
                                                               'PRIORITY', self.DEM)
                        self.arcpy.DeleteField_management(line[0], ['PRIORITY'])
                    # else:
                    #     self.arcpy.PolygonToRaster_conversion(line[0], line[1], featureName, 'MAXIMUM_COMBINED_AREA',
                    #                                           '', self.DEM)
                    featureName = self.arcpy.Raster(featureName)
            self.gridded_layers.append(featureName)
        self.gridded_layers.reverse()

    def _get_raster_extension(self):
        if '.gdb' in self.workspace:
            self.ras_ext = ''
        else:
            self.ras_ext = '.tif'


if __name__ == '__main__':
    base = r'C:\CODE\CostSurface\TestingData'
    feature_list = [(base + r'\Streams.shp', 'cost'),
                    (base + r'\Roads.shp', 'Speed_mph'),
                    (base + r'\Vegetation.shp', 'cost')]
    DEM = base + r'\DEM'
    workspace = r'C:\CODE\CostSurface\scratch'

    cs = feature_stacker(
        feature_list=feature_list
        , DEM=DEM
        , workspace=workspace)

    c = cs.create()
    c.save(workspace + r'\feature_stacker.tif')
