"""System for storing and randomly picking an ingame event to happen"""

import random

class EventStream:
    def __init__(self, events = None):
        # 'nothing happens' events
        self.events = [None for e in range(30)]

        # actual initial events
        if events:
            self.events += events

    def pick_event(self):
        return self.events[random.randrange(len(self.events))]

    def add(self, event):
        self.events.append(event)