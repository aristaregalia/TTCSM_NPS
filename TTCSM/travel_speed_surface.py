from TTCSM.feature_stacker import feature_stacker as fs
from TTCSM.digital_elevation_model import digital_elevation_model as dm
from TTCSM.trail_speed_surface import trail_speed_surface
from TTCSM.network_speed_surface import network_speed_surface as nss
from TTCSM.base_speed_surface import base_speed_surface as bss
from TTCSM.root import root
from TTCSM.unit_converter import unit_converter as uc


class travel_speed_surface(root):
    """
        The travel speed surface is a grid that represents the
        velocity (seconds per meter) of a person traveling. Modes of travel
        can include moving over a road network with a motorized vehicle
        (network speed), walking on a trail (trail speed)
        , or walking off a trail (base speed).

        STEPS:
            1.Create
                a.Network (motorized) Speed Surface
                b.Masked areas too steep for foot travel
                c.Trail Speed Surface
                d.Base Speed Surface (lakes, streams, landcover)
            2.Stack Layers in respective order;  network speed surface on top
                and base speed surface on bottom

        RETURNS
        Raster object representing travel speed in seconds per meter

        """

    def __init__(self,
                 DEM,
                 maximum_slope=31,
                 base_layers=None,
                 network_layers=None,
                 trail_layers=None,
                 walking_speed_mph=3.1,
                 workspace=None):
        super(travel_speed_surface, self).__init__(workspace=workspace, DEM=DEM)
        self.base_layers = base_layers
        self.network_layers = network_layers
        self.trail_layers = trail_layers
        self.maximum_slope = maximum_slope
        self.walking_speed_mph = walking_speed_mph

        self.network_speed_surface = None
        self.trail_speed_surface = None
        self.base_speed_surface = None
        self.layers = []

    def create(self):
        self._create_network_speed_surface()
        self._create_trail_speed_surface()
        self._create_steep_areas_mask()  # this masks all the layers created afer this
        self._create_base_speed_surface()
        self._stack_layers()
        self._set_Nulls()
        self._scale_by_units()
        return self.stacked_layers

    def _scale_by_units(self):
        """If units are in feet, converts to meters
            since the final resulting grid is seconds/meter"""
        if self.dem.xy_units == 'Undefined':
            cmn.quit('Terminating: Undefined DEM Units')
        elif self.dem.xy_units == 'Foot':
            sv = uc(self.stacked_layers)
            self.stacked_layers = sv.feet_to_meters()

    def _create_subsurface(self):
        """
            Ensures that there is a subsurface layer that maintains the extent
            of the DEM. Without this, cost surfaces are limited to the extent
            of other features.
            """
        #d = dm.digital_elevation_model(self.DEM)
        d = dm(self.DEM)
        subsurface = [d.get_constant_surface_of_ones(), '']
        if self.base_layers is None:
            self.base_layers = ([subsurface])
        else:
            self.base_layers.append(subsurface)

    def _create_base_speed_surface(self):
        self._create_subsurface()
        #b = bss.base_speed_surface(
        b = bss(
            base_layers=self.base_layers
            , DEM=self.DEM
            , workspace=self.workspace
            , walking_speed_mph=self.walking_speed_mph)
        self.base_speed_surface = b.create()
        self.layers.append([self.base_speed_surface, 'value'])

    def _create_network_speed_surface(self):
        if self.network_layers is not None:
            #n = nss.network_speed_surface(
            n = nss(
                network_layers=self.network_layers
                , DEM=self.DEM
                , workspace=self.workspace)
            self.network_speed_surface = n.create()
            self.layers.append([self.network_speed_surface, 'value'])

    def _create_trail_speed_surface(self):
        if self.trail_layers is not None:
            #t = trail_speed_surface.trail_speed_surface(
            t = trail_speed_surface(
                trail_layers=self.trail_layers
                , DEM=self.DEM
                , walking_speed_mph=self.walking_speed_mph
                , workspace=self.workspace
                , max_slope_cap=self.maximum_slope)
            self.trail_speed_surface = t.create()
            self.layers.append([self.trail_speed_surface, 'value'])

    def _create_steep_areas_mask(self):
        #self.dem = dm.digital_elevation_model(self.DEM)
        self.dem = dm(self.DEM)
        self.steep_mask = self.dem.get_unwalkable_mask(self.maximum_slope)
        self.layers.append([self.steep_mask, 'value'])

    def _stack_layers(self):

        #final_stack = fs.feature_stacker(self.layers, self.DEM, self.workspace)
        final_stack = fs(self.layers, self.DEM, self.workspace)
        self.stacked_layers = final_stack.create()

    def _set_Nulls(self):
        """Ideally, barriers such as lakes and steep areas should be masked out as Null/NoData. However, this is not working
            properly (ArcGIS 10.2.2) and is confusing the cost distance calculations. Therefore, barriers are set to an extremely slow
            travel speed. """
        self.stacked_layers = self.arcpy.sa.Con(self.arcpy.sa.GreaterThan(self.stacked_layers, 0), self.stacked_layers,
                                                1000000)


if __name__ == '__main__':
    from .unit_converter import unit_converter as uc

    base = 'C:\\CODE\\CostSurface\\TestingData\\'
    workspace = 'C:\\TEMP'

    base_layers = [
        (base + 'Streams.shp', 'PMTS'),
        (base + 'Landcover.shp', 'PMTS')]
    network_layers = [(base + 'Roads.shp', 'Speed_mph')]
    trail_layers = [(base + 'Trails.shp', 'PMTS')]
    maximum_slope = 20
    DEM = base + 'dem'

    walking_speed_mph = 3

    tss = travel_speed_surface(
        base_layers=base_layers,
        network_layers=network_layers,
        trail_layers=trail_layers,
        maximum_slope=maximum_slope,
        DEM=DEM,
        workspace=workspace
        , walking_speed_mph=walking_speed_mph)

    travSurf = tss.create()
    travSurf.save(workspace + '\\travel_speed_surface_secM.img')

    s = uc(travSurf)
    spd_mph = s.secondsMeter_to_milesHour()
    spd_mph.save(workspace + '\\travel_speed_surface_mpH.img')

    # reconvert back to SecM
    rc = uc(spd_mph)
    redo = rc.milesHour_to_secondsMeter()
    redo.save(workspace + '\\travel_speed_surface_secM_redo.img')
