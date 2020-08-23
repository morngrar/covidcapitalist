"""System for production"""

import time

deltatime = 0
last_time = 0


# How much each factory costs to build
factory_cost = {
    "mask factories": 100,
    "glove factories": 500,
    "antibac factories": 100,
    "visir factories": 550,
    "ventilator factories": 1000,
    "toilet-paper factories": 350,
}

# Mow much each factory will add to production
factory_production_rate = {
    "mask factories": 5,
    "glove factories": 10,
    "antibac factories": 10,
    "visir factories": 7,
    "ventilator factories": 5,
    "toilet-paper factories": 15,
}


def add_factory(game_data, factory):
    if game_data["cash"] >= factory_cost[factory]:
        game_data[factory] += 1
        game_data["cash"] -= factory_cost[factory]
        return True
    else:
        return False


def produce(game_data):
    global deltatime
    global last_time
    now = time.time()
    deltatime += now - last_time
    last_time = now
    factory_keys = [key for key in game_data.keys() if 'factories' in key]

    if deltatime >= 1:
        deltatime = 0

        for factory in factory_keys:
            item = factory.split()[0] + " stock"
            game_data[item] += factory_production_rate[factory] * game_data[factory]  # Add to stock
