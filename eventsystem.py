"""System for storing and randomly picking an ingame event to happen"""

import random
import time

NOTHING_CHANCE = 3
EVENT_INTERVAL = 5   # value in seconds

class Event:
    def __init__(self, text, data):
        """data is a dict of game values that will be added to current game data"""
        self.text = text
        self.data = data


class EventStream:
    def __init__(self, events = None):
        # 'nothing happens' events
        self.events = [None for e in range(NOTHING_CHANCE)]

        # actual initial events
        if events:
            self.events += events

        self.delta = 0
        self.last_time = time.time()
    
    def time_for_event(self):
        """Called in game loop, returns true if time for event"""
        now = time.time()
        self.delta += now - self.last_time
        self.last_time = now

        if self.delta >= EVENT_INTERVAL:
            self.delta = 0
            return True

        return False
        
    def pick_event(self):
        """Picks a random event and returns it"""
        return self.events[random.randrange(len(self.events))]

    def add(self, event):
        self.events.append(event)


def update_game_data(event, game_data):
    """Takes an event and a reference to the global game state

    Updates game state additively according to event
    """
    for k, v in event.data.items():
        game_data[k] += v
