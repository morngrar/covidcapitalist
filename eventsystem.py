"""System for storing and randomly picking an ingame event to happen"""

import random
import time

NOTHING_CHANCE = 10
EVENT_INTERVAL = 1   # value in seconds

class Event:
    def __init__(self, text, data, oneoff=False):
        """data is a dict of game values that will be added to current game data"""
        self.text = text
        self.data = data
        self.oneoff = oneoff


class EventStream:
    def __init__(self, events = None):
        # 'nothing happens' events
        self.events = [None for e in range(NOTHING_CHANCE)]

        # built-in events
        self.events += [
            Event(
                "A toilet-paper warehouse in Tulpa burned down! Demand +200",
                {
                    "toilet-paper demand" : 200,
                }
            ),
            Event(
                "A toilet-paper warehouse in Stockholm burned down! Demand +50",
                {
                    "toilet-paper demand" : 50,
                }
            ),
            Event(
                "A toilet-paper warehouse in Rome burned down! Demand +100",
                {
                    "toilet-paper demand" : 100,
                }
            ),
            Event(
                "A toilet-paper warehouse in Raufoss burned down! Demand +150",
                {
                    "toilet-paper demand" : 150,
                }
            ),
            Event(
                "Stock decreased in value! You lose $30000",
                {
                    "cash" : -30000,
                }
            ),
            Event(
                "Stock decreased in value! You lose $10000",
                {
                    "cash" : -10000,
                }
            ),
            Event(
                "One of your mask factories was destroyed during a conspiracy-theorist attack!",
                {
                    "mask factories" : -1,
                }
            ),
            Event(
                "One of your antibac factories exploded!",
                {
                    "antibac factories" : -1,
                }
            ),
            Event(
                "One of your ventilator factories burned down!",
                {
                    "ventilator factories" : -1,
                }
            ),
            Event(
                "One of your toilet paper factories !",
                {
                    "ventilator factories" : -1,
                }
            ),
            Event(
                "Some gloves got lost in transport! Glove stock -100",
                {
                    "glove stock" : -100,
                }
            ),
            Event(
                "Some masks got lost in transport! Mask stock -50",
                {
                    "mask stock" : -50,
                }
            ),
            Event(
                "Some antibac got lost in transport! Antibac stock -25",
                {
                    "antibac stock" : -25,
                }
            ),
            Event(
                "Some visirs got lost in transport! Visir stock -30",
                {
                    "visir stock" : -30,
                }
            ),
            Event(
                "A ventilator was replaced by warranty!",
                {
                    "ventilator stock" : -1,
                }
            ),
            Event(
                "A a recent ad-campaign of yours went viral! Renown +3%",
                {
                    "renown" : 3,
                }
            ),
            Event(
                "Anti-maskers are spreading their fake news! Mask demand -5000",
                {
                    "mask demand" : -5000,
                }
            ),
            Event(
                "Soap producers claim soap is more effective than antibac! Antibac demand -3000",
                {
                    "antibac demand" : -3000,
                }
            ),
            Event(
                "Greece needs many ventilators for their new emergency hospital!",
                {
                    "ventilator demand" : 100,
                }
            ),
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
        index = random.randrange(len(self.events))
        event = self.events[index]
        if event and event.oneoff:
            del self.events[index]
        return event

    def add(self, event):
        self.events.append(event)


def update_game_data(event, game_data):
    """Takes an event and a reference to the global game state

    Updates game state additively according to event
    """
    for k, v in event.data.items():
        if game_data[k] + v < 0:    # Prevent negative numbers of factories, stock or demand
            return False
            
    for k, v in event.data.items():
        game_data[k] += v

    return True
