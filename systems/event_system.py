from utils.esper import Processor
from utils.time_schedule import TimeSchedule
from components.action import Action


class EventSystem(Processor):
    def __init__(self):
        super().__init__()
        self.turn_scheduler = TimeSchedule()

    def process(self, *args, **kwargs):
        print(f'Event System {self.world.timer=}'.center(100, '#'))
        for ent, act in self.world.get_component(Action):
            if ent not in self.turn_scheduler.scheduled_events.queue:
                print(f'Add {ent.name} with {act.cost=} to scheduler')
                self.turn_scheduler.schedule_event(ent, act.cost)

        print(f'Current turn queue on turn {self.world.timer}')
        print(f'{self.turn_scheduler.next_key().name=}, {self.turn_scheduler.next_key().uid=}')
        for ind, (ent, val) in enumerate(self.turn_scheduler.scheduled_events.queue.items()):

            print(f'{ind} {ent.name=}, {val=}')
