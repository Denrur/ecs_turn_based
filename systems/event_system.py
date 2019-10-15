from utils.esper import Processor
from utils.time_schedule import TimeSchedule
from components.action import Action


class EventSystem(Processor):
    def __init__(self):
        super().__init__()
        self.turn_scheduler = TimeSchedule()

    def process(self, *args, **kwargs):
        for ent, act in self.world.get_component(Action):
            if ent not in self.turn_scheduler.scheduled_events.queue:
                self.turn_scheduler.schedule_event(ent, act.cost)

        for ent, val in self.turn_scheduler.scheduled_events.queue.items():
            print(ent.name, val)
