from TTCSM.root import root
import TTCSM.common as cmn
import re


class digital_elevation_model(root):
    def __init__(self, DEM_path, workspace=None):
        super(digital_elevation_model, self).__init__(workspace=workspace, DEM=DEM_path)
        if not isinstance(DEM_path, self.arcpy.Raster):
            self.DEM_path = self.arcpy.sa.Raster(DEM_path)
        else:
            self.DEM_path = DEM_path

        # Raster Attributes (should be pushed up to a RASTER class)
        self.x_cell_size = None
        self.y_cell_size = None
        self.yMax = None
        self.xMin = None
        self.xMax = None
        self.yMin = None
        self.xy_units = None

        self._initiaze_grid_values()
        self._set_XY_Units()

    def _set_XY_Units(self):
        """
        Gets and sets xy_units for X and Y dimensions
        """
        spatial_ref = self.arcpy.Describe(self.DEM_path).spatialReference
        info = spatial_ref.exporttostring()
        p = re.compile(r'Meter')
        hasMeter = p.search(info)
        p = re.compile(r'Foot')
        hasFeet = p.search(info)
        if (hasFeet is not None and hasMeter is not None) or (hasFeet is None and hasMeter is None):
            self.xy_units = 'Undefined'
        elif hasMeter is not None:
            self.xy_units = 'Meter'
        else:
            self.xy_units = 'Feet'

    def get_constant_surface_of_zeros(self):
        """
        Returns AOA as a constant layer of Zeros
        """
        return self.arcpy.sa.IsNull(self.DEM_path)

    def get_constant_surface_of_ones(self):
        """
        Returns AOA as a constant layer of Zeros
        """
        grid = self.get_constant_surface_of_zeros()
        g2 = self.arcpy.sa.Con(grid == 0, 1)
        return g2

    def get_degree_slope(self, max_slope_cap=None):
        """
        Returns the file path for a grid containing
            the slope, in degreess, calculated from the DEM
        If the max_slope_cap is specified, then the slope is capped to that
            value
        """
        ds = self.arcpy.sa.Slope(self.DEM_path, "DEGREE")
        if max_slope_cap is not None and max_slope_cap > 0 and max_slope_cap < 90:
            ds = self.arcpy.sa.Con(ds > max_slope_cap, max_slope_cap, ds)
        return ds

    def get_unwalkable_slope_surface(self, maximum_slope):
        """
        Returns a True/False surface indicating whether the slope is GTE
        the maximum specified for walking.
        0 = Walkable
        1 = Unwalkable

        """
        ds = self.get_degree_slope()
        return self.arcpy.sa.GreaterThanEqual(ds, maximum_slope)

    def get_unwalkable_mask(self, maximum_slope):
        """
        Returns a mask indicating whether the slope is
        greater than or equal to the maximum specified for walking. Unwalkable
        areas are set to 0. Walkable areas are set as NoData

        If outFile is specified, creates the respective file
        """
        unwalkable = self.get_unwalkable_slope_surface(maximum_slope)
        return self.arcpy.sa.SetNull(unwalkable == 0, 0)

    def _initiaze_grid_values(self):

        self.x_cell_size = float(str(self.arcpy.GetRasterProperties_management(self.DEM_path, "CELLSIZEX")))
        self.y_cell_size = float(str(self.arcpy.GetRasterProperties_management(self.DEM_path, "CELLSIZEY")))
        self.yMax = float(str(self.arcpy.GetRasterProperties_management(self.DEM_path, "TOP")))
        self.xMin = float(str(self.arcpy.GetRasterProperties_management(self.DEM_path, "LEFT")))
        self.xMax = float(str(self.arcpy.GetRasterProperties_management(self.DEM_path, "RIGHT")))
        self.yMin = float(str(self.arcpy.GetRasterProperties_management(self.DEM_path, "BOTTOM")))


if __name__ == '__main__':
    workspace = r'C:\TEMP'
    d = digital_elevation_model('C:\\CODE\\CostSurface\\TestingData\\dem', workspace=workspace)
    # max_slope = 5
    # print str(d.x_cell_size)
    # print str(d.y_cell_size)

    # Calculate slope of DEM and optionally set the maximum slope to be capped
    a = d.get_degree_slope(max_slope_cap=6)
    print(a)

##
#    test = d.get_unwalkable_mask(max_slope)
#    test.save('C:\\CODE\\CostSurface\\scratch\\unwalkable_mask.tif')
#
#    test = d.get_unwalkable_slope_surface(max_slope)
#    test.save('C:\\CODE\\CostSurface\\scratch\\unwalkable_slope_surface.tif')
#
#    test = d.get_degree_slope()
#    test.save('C:\\CODE\\CostSurface\\scratch\\degree_slope.tif')
##
#    test = d.get_constant_surface_of_ones()
#    test.save('C:\\CODE\\CostSurface\\scratch\\ones.tif')
