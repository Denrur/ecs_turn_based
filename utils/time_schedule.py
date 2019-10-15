from pqdict import pqdict


class PriorQueue:
    def __init__(self):
        self.queue = pqdict()

    def __len__(self):
        return len(self.queue)

    def keys(self):
        return self.queue.keys()

    def enqueue(self, value, priority=0.0):
        self.queue[value] = priority

    def adjust_priority(self, add):
        for v in self.queue:
            self.queue[v] += add

    def dequeue(self):
        return self.queue.pop()

    def dequeue_with_key(self):
        return self.queue.popitem()

    def erase(self, value):
        del self.queue[value]

    def top(self):
        return self.queue.top()


class TimeSchedule:
    def __init__(self):
        self.scheduled_events = PriorQueue()

    def __len__(self):
        return len(self.scheduled_events)

    def keys(self):
        return self.scheduled_events.keys()

    def schedule_event(self, event, delay=0.0):
        if event is not None:
            self.scheduled_events.enqueue(event, delay)

    def next_event(self):

        event, time = self.scheduled_events.dequeue_with_key()
        self.scheduled_events.adjust_priority(-time)

        return event

    def next_key(self):
        return self.scheduled_events.top()

    def cancel_event(self, event):

        self.scheduled_events.erase(event)
