import utils.esper as esper
from components.action import Action
from components.damager import Damager
from components.condition import Condition
from components.game_map import GameMap
from components.health import Health
from components.joystick import Joystick
from components.physics import Physics
from components.position import Position
from components.renderable import Renderable

from systems.action_processor import ActionProcessor
from systems.condition_process import ConditionProcessor
from systems.map_processor import MapProcessor


def move(pos, phys):
    pos.x += phys.x
    pos.y += phys.y
    phys.x = 0
    phys.y = 0
    phys.move = False


class PhysicProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, *args, **kwargs):
        print(f'Physic processor {self.world.timer=}'.center(100, '#'))
        map_ = self.world.get_processor(MapProcessor).current_map
        ent = self.world.get_processor(ActionProcessor).current_entity
        action = self.world.component_for_entity(ent, Action)

        phys = self.world.component_for_entity(ent, Physics)
        pos = self.world.component_for_entity(ent, Position)
        dmg = self.world.component_for_entity(ent, Damager)
        # entities = [k for k, v in self.world.get_component(Position)
        #             if (v.x, v.y) == (pos.x + phys.x, pos.y + phys.y)]

        print(f'''{ent.name=}, {action.type=}, {action.cost=}, {pos.x=}, {pos.y=},
        {phys.x=}, {phys.y=}''')
        if action.type == 'move':
            entities = map_.entities_positions.get((pos.x + phys.x, pos.y + phys.y))
            if entities:
                print(f'move {entities=}')
                for entity in entities:
                    if self.world.has_component(entity, Physics):
                        if self.world.component_for_entity(entity, Physics).collidable:
                            phys.move = False
                            action.type = 'attack'
                            dmg.attack = True
                            dmg.x, dmg.y = phys.x, phys.y
                            print(f'{ent.name=} {action.type=} {action.flag=}')
                effects = self.world.component_for_entity(ent, Condition)
                # print(f'{ent.name} {list(effects.conditions_list)}')
                if ConditionProcessor.stun_effect in effects.conditions_list:
                    phys.move = False
                    print(f'           not moving {ent.name=} {phys.move=}')
                if phys.move:
                    rend = self.world.component_for_entity(ent, Renderable)
                    rend.x += phys.x
                    rend.y += phys.y
                    move(pos, phys)
                    print(f'{ent.name=} {pos.x=} {pos.y=} ')
        if action.type == 'attack':
            print(f'{dmg.x=} {dmg.y=}')
            tar_x, tar_y = dmg.x, dmg.y
            entities = map_.entities_positions.get((pos.x + tar_x, pos.y + tar_y))
            if entities:
                print(f' attack {entities=}')
                for entity in entities:
                    if self.world.has_component(entity, Joystick):
                        pass
                    else:
                        self.world.get_processor(ConditionProcessor).add_effect(entity, ConditionProcessor.stun_effect, 20)
                    if self.world.has_component(entity, Health):
                        health = self.world.component_for_entity(entity, Health)
                        health.hp -= dmg.power
                        print(f'{ent.name=} hit {entity.name=} with {dmg.power=}, {entity.name=} left {health.hp=}')
                        if health.hp <= 0:
                            self.world.get_processor(ConditionProcessor).add_effect(entity,
                                                                                    ConditionProcessor.death_condition, -1)
                            print(f'{self.world.components_for_entity(entity)=}')
                    else:
                        print(f'{ent.name} can\'t hurt {entity.name}')
