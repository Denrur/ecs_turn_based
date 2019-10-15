from utils.esper import Processor
from systems.event_system import EventSystem
from components.action import Action
from components.damager import Damager
from components.physics import Physics
from utils.decorators import debug_info


class ActionProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.current_entity = None

    @debug_info
    def process(self):
        scheduler = self.world.get_processor(EventSystem).turn_scheduler
        ent = scheduler.next_event()

        action = self.world.component_for_entity(ent, Action)

        if action.type == 'move':
            phys = self.world.component_for_entity(ent, Physics)
            phys.x, phys.y = action.param
            phys.move = action.flag
        if action.type == 'attack':
            dmg = self.world.component_for_entity(ent, Damager)
            dmg.target = action.param
            dmg.attack = action.flag
        self.current_entity = ent



