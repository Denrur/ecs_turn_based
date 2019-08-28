import utils.esper as esper
from components.fov import Fov
from components.position import Position
from components.renderable import Renderable
from components.physics import Physics
from systems.map_processor import MapProcessor
from utils import rpas
from utils.decorators import benchmark


class FovProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    @benchmark
    def process(self):
        print('Fov processor')
        for ent, (fov, pos) in self.world.get_components(Fov, Position):
            if fov.recalc_fov:
                self.world.get_processor(MapProcessor).get_entities_positions()
                print('Calc fov')
                fov.cells = self.calc_fov(pos.x, pos.y, fov.radius)
                fov.recalc_fov = False

    def calc_fov(self, x, y, radius):
        fov = rpas.FOVCalc()
        is_unobstruct = self.is_unobstruct
        return fov.calc_visible_cells_from(x, y, radius, is_unobstruct)

    def is_unobstruct(self, x, y):
        entities = self.world.get_processor(MapProcessor).current_map.entities_positions.get((x, y))
        for entity in entities:
            if not self.world.component_for_entity(entity, Renderable).trans:
                return False
        return True
