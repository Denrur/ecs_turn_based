import utils.esper as esper
from components.joystick import Joystick
from components.action import Action
from systems.event_system import EventSystem
from bearlibterminal import terminal as blt


class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print(f'Input processor {self.world.timer=}')
        scheduler = self.world.get_processor(EventSystem).turn_scheduler

        for ent, ctrl in self.world.get_component(Joystick):
            print(f'{scheduler.next_key().name=}, {scheduler.next_key().uid=}')

            if ent == scheduler.next_key():
                key = blt.read()

                print(ent.name, 'Have input', key)

                action = self.world.component_for_entity(ent, Action)

                for k, v in ctrl.handle_player_turn_keys(key).items():
                    action.type = k
                    action.param = v
                    action.flag = True

                scheduler.schedule_event(ent, action.cost)

        for ent_, val in scheduler.scheduled_events.queue.items():
            print(f'{ent_.name=}, {val=}')
