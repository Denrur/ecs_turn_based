import utils.esper as esper
from components.joystick import Joystick
from components.action import Action
from systems.event_system import EventSystem
from bearlibterminal import terminal as blt
from utils.decorators import benchmark


class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    # @benchmark
    def process(self):
        print('Input processor')
        scheduler = self.world.get_processor(EventSystem).turn_scheduler
        for ent, ctrl in self.world.get_component(Joystick):
            print(scheduler.next_key().uid)
            if ent == scheduler.next_key():
                key = blt.read()
                print(ent.uid, 'Have input', key)

                action = self.world.component_for_entity(ent, Action)
                for k, v in ctrl.handle_player_turn_keys(key).items():
                    action.type = k
                    action.param = v
                    action.flag = True
                    if key == 22:
                        action.cost = 1
                # if ent not in scheduler.scheduled_events.queue:
                scheduler.schedule_event(ent, action.cost)
                for ent, val in scheduler.scheduled_events.queue.items():
                    print(ent.uid, val)
