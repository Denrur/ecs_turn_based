from utils.esper import Processor
from systems.event_system import EventSystem
from components.action import Action
from components.damager import Damager
from components.physics import Physics


class ActionProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.current_entity = None

    def process(self):
        print(f'Action Processor {self.world.timer=}')
        scheduler = self.world.get_processor(EventSystem).turn_scheduler
        ent = scheduler.next_event()

        action = self.world.component_for_entity(ent, Action)

        if action.type == 'move':
            phys = self.world.component_for_entity(ent, Physics)
            phys.x, phys.y = action.param
            phys.move = action.flag
        if action.type == 'attack':
            dmg = self.world.component_for_entity(ent, Damager)
            dmg.x, dmg.y = action.param
            dmg.attack = action.flag
        self.current_entity = ent
        print(f'{ent.name=}, {action.type=}')





