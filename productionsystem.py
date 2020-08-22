"""System for production"""

import time

deltatime = 0
last_time = 0

# How much each factory costs to build
factory_cost = {
    "mask factories": 100,
    "glove factories": 500,
    "antibac factories": 2000,
    "visir factories": 5000,
    "ventilator factories": 10000,
    "tp factories": 3500,
}

# Mow much each factory will add to production
factory_production_rate = {
    "mask factories": 5,
    "glove factories": 10,
    "antibac factories": 10,
    "visir factories": 7,
    "ventilator factories": 5,
    "tp factories": 15,
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
    print("DELTA: ", deltatime)
    print("NOW: ", now)

    if deltatime >= 1:
        print(deltatime)
        deltatime = 0
