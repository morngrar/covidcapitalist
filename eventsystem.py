"""System for storing and randomly picking an ingame event to happen"""

import random
import time

NOTHING_CHANCE = 3
EVENT_INTERVAL = 1   # value in seconds

class Event:
    def __init__(self, text, data):
        """data is a dict of game values that will be added to current game data"""
        self.text = text
        self.data = data


class EventStream:
    def __init__(self, events = None):
        # 'nothing happens' events
        self.events = [None for e in range(NOTHING_CHANCE)]

        # built-in events
        self.events += [
            Event(
                "A toilet-paper warehouse in Tulpa burned down!",
                {
                    "toilet-paper demand" : 2000,
                }
            ),
            Event(
                "One of your mask factories was destroyed during a conspiracy-theorist attack!",
                {
                    "mask factories" : -1,
                }
            ),
            Event(
                "Your great great aunt passed away! She left you a small fortune",
                {
                    "cash" : 10000,
                }
            ),
            Event(
                "Some gloves got lost in transport!",
                {
                    "glove stock" : -50,
                }
            ),
            Event(
                "Some masks got lost in transport!",
                {
                    "mask stock" : -100,
                }
            ),
            Event(
                "Some antibac got lost in transport!",
                {
                    "antibac stock" : -25,
                }
            ),
            Event(
                "Your office got water damage!",
                {
                    "cash" : -300,
                }
            ),
            Event(
                "Some visirs got lost in transport!",
                {
                    "visir stock" : -30,
                }
            ),
            Event(
                "A ventilator was replaced by warranty!",
                {
                    "ventilator stock" : -1,
                }
            )
        ]

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
        print("K", k)
        print("V", v)
        if game_data[k] + v > -1:    # Prevent negative numbers of factories, stock or demand
            game_data[k] += v
            return True
        else:
            return False
