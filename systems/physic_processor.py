import utils.esper as esper
from components.action import Action
from components.damager import Damager
from components.effects import Effects
from components.health import Health
from components.physics import Physics
from components.position import Position
from components.renderable import Renderable

from systems.action_processor import ActionProcessor
from systems.effect_processor import EffectProcessor
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
        print(f'Physic processor {self.world.timer=}')
        ent = self.world.get_processor(ActionProcessor).current_entity
        action = self.world.component_for_entity(ent, Action)

        phys = self.world.component_for_entity(ent, Physics)
        pos = self.world.component_for_entity(ent, Position)
        dmg = self.world.component_for_entity(ent, Damager)
        entities = [k for k, v in self.world.get_component(Position)
                    if (v.x, v.y) == (pos.x + phys.x, pos.y + phys.y)]

        print(f'{ent.name=}, {action.type=}, {action.cost=}')
        if action.type == 'move':
            for entity in entities:
                if self.world.has_component(entity, Physics):
                    if self.world.component_for_entity(entity, Physics).collidable:
                        phys.move = False
                        action.type = 'attack'
                        dmg.attack = True
                        dmg.x, dmg.y = phys.x, phys.y
                        print(f'{ent.name=} {action.type=} {action.flag=}')
            if phys.move:
                rend = self.world.component_for_entity(ent, Renderable)
                rend.x += phys.x
                rend.y += phys.y
                move(pos, phys)
                print(f'{ent.name=} {pos.x=} {pos.y=} ')
        if action.type == 'attack':
            print(f'{dmg.x=} {dmg.y=}')
            tar_x, tar_y = dmg.x, dmg.y
            entities = [k for k, v in self.world.get_component(Position)
                        if (v.x, v.y) == (pos.x + tar_x, pos.y + tar_y)]
            for entity in entities:
                if self.world.has_component(entity, Health):
                    health = self.world.component_for_entity(entity, Health)
                    health.hp -= dmg.power
                    print(f'{ent.name=} hit {entity.name=} with {dmg.power=}, {entity.name=} left {health.hp=}')
                    if health.hp <= 0:
                        self.world.get_processor(EffectProcessor).add_effect(entity, 'death', -1)
                        print(f'{self.world.components_for_entity(entity)=}')
                else:
                    print(f'{ent.name} can\'t hurt {entity.name}')