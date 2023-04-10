from .root import root


class unit_converter(root):
    def __init__(self, grid, workspace=None):
        super(unit_converter, self).__init__(workspace=workspace, DEM=grid)
        if isinstance(grid, self.arcpy.Raster):
            self.grid = grid
        else:
            self.grid = arcpy.sa.Raster(grid)
        grid = self.arcpy.sa.Float(grid)

    def secondsMeter_to_milesHour(self):
        """convert seconds/meter to miles/hour"""
        return (0.62137119 * .001 * 3600) / self.grid

    def milesHour_to_secondsMeter(self):
        """ Converts from miles/per hour to seconds/per meter """
        return 3600 / ((self.grid * 1.60934) * 1000)

    def feet_to_meters(self):
        return self.grid / 3.28084

    def seconds_to_mins(self):
        return self.grid / 60

    def seconds_to_hours(self):
        return self.grid / 3600


if __name__ == '__main__':
    grid = 'C:\\CODE\\CostSurface\\scratch\\base_speed_surface.tif'
    uc = unit_converter(grid)
    mph = uc.secondsMeter_to_milesHour()
    mph.save('C:\\CODE\\CostSurface\\scratch\\mph.tif')
