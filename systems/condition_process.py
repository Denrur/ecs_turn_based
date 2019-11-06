from utils.esper import Processor
from components.condition import Condition
from components.ai import Ai
from components.action import Action
from components.item import Item
from components.renderable import Renderable
from components.physics import Physics
from systems.event_system import EventSystem
from utils.layers import Layers


class ConditionProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print(f'ConditionProcessor {self.world.timer=}'.center(100, '#'))
        for entity, conditions in self.world.get_component(Condition):
            active_conditions = self.proceed(entity, conditions.conditions_list)
            for condition in active_conditions:
                condition(self, entity)
            # print(f' Effects on {entity.name=} {active_conditions=}')

    def add_effect(self, entity, effect, duration=-1, power=None):
        # print(f'add {effect=} to {entity.name=}')
        if self.world.has_component(entity, Condition):
            cond = self.world.component_for_entity(entity, Condition)
            if cond not in cond.conditions_list:
                cond.conditions_list[effect] = [duration, power]

    def remove_condition(self, entity, condition):
        conditions = self.world.component_for_entity(entity, Condition)
        if conditions.conditions_list[condition]:
            del conditions.conditions_list[condition]

    def proceed(self, entity, conditions):
        for cond in list(conditions):
            if conditions[cond][0] > 0:
                conditions[cond][0] -= 1
                if conditions[cond][0] == 0:
                    self.remove_condition(entity, cond)
        return conditions.keys()

    def death_condition(self, entity):
        print(f'{entity.name=} dead')
        for component in (Ai, Action):
            if self.world.has_component(entity, component):
                self.world.remove_component(entity, component)
        if entity in self.world.get_processor(EventSystem).turn_scheduler.keys():
            self.world.get_processor(EventSystem).turn_scheduler.cancel_event(entity)

        rend = self.world.component_for_entity(entity, Renderable)

        rend.char = 'x'
        rend.layer = Layers.CORPSES
        phys = self.world.component_for_entity(entity, Physics)
        phys.collidable = False
        self.world.add_component(entity, Item(coast=5, weight=4))

    def stun_effect(self, entity):
        phys = self.world.component_for_entity(entity, Physics)
        phys.move = False



