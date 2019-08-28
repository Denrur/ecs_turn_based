import utils.esper as esper
from components.action import Action
from components.damager import Damager
from components.physics import Physics
from components.position import Position
from systems.action_processor import ActionProcessor
from components.renderable import Renderable
from utils.decorators import benchmark


def move(pos, phys):
    pos.x += phys.x
    pos.y += phys.y
    phys.x = 0
    phys.y = 0
    phys.move = False


class PhysicProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    # @benchmark
    def process(self, *args, **kwargs):
        print('Physic processor')
        ent = self.world.get_processor(ActionProcessor).current_entity
        # for ent in entities_order:
        action = self.world.component_for_entity(ent, Action)
        print(ent.uid, action.type, action.cost)
        if action.type == 'move':
            phys = self.world.component_for_entity(ent, Physics)
            pos = self.world.component_for_entity(ent, Position)
            if phys.move:
                entities = [k for k, v in self.world.get_component(Position)
                            if (v.x, v.y) == (pos.x + phys.x, pos.y + phys.y)]
                for entity in entities:
                    if self.world.has_component(entity, Physics):
                        if self.world.component_for_entity(entity, Physics).collidable:
                            phys.move = False
                            print(f'{entity.name} {entity.uid} cannot be passed')
                            break
                else:
                    rend = self.world.component_for_entity(ent, Renderable)
                    rend.x += phys.x
                    rend.y += phys.y
                    move(pos, phys)
        elif action.type == 'attack':
            pos = self.world.component_for_entity(ent, Position)
            dmg = self.world.component_for_entity(ent, Damager)
            if dmg.attack:
                tar_x, tar_y = dmg.target
                entities = [k for k, v in self.world.get_component(Position)
                            if (v.x, v.y) == (pos.x + tar_x, pos.y + tar_y)]
                for entity in entities:
                    print(f'{ent.uid} hit {entity.uid} with {dmg.power}')
