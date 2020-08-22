import pygame

from hello import hello, event_glob_test
from warehouse import checkWarehouse, increaseDemand
from eventsystem import EventStream
from productionsystem import add_factory, produce
import eventsystem

# global variables
market_events = eventsystem.EventStream()
game_data = {
    "renown" : 50,
    "cash" : 1000,

    #stock
    "mask stock" : 0,
    "glove stock" : 0,
    "antibac stock" : 0,
    "visir stock" : 0,
    "ventilator stock" : 0,
    "toilet-paper stock" : 0,

    # demand
    "mask demand" : 0,
    "glove demand" : 0,
    "antibac demand" : 0,
    "visir demand" : 0,
    "ventilator demand" : 0,
    "toilet-paper demand" : 0,

    #price
    "mask price" : 0,
    "glove price" : 0,
    "antibac price" : 0,
    "visir price" : 0,
    "ventilator price" : 0,
    "toilet-paper price" : 0,

    # factories
    "mask factories" : 0,
    "glove factories" : 0,
    "antibac factories" : 0,
    "visir factories" : 0,
    "ventilator factories" : 0,
    "toilet-paper factories" : 0,


    # off the books production
    "moonshine producers" : 0,
}

def main():
    """The games main loop"""

    HIDPI = True
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1280
    EVENT_FONT_SIZE = 16

    pygame.init()

    if HIDPI:
        SCREEN_HEIGHT *= 2
        SCREEN_WIDTH *= 2
        EVENT_FONT_SIZE *= 2

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption("COVID Capitalist")
    pygame.display.update()

    increaseDemand(game_data)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(game_data)
                elif event.key == pygame.K_f:
                    # increment all factories by one on f-keypress
                    factories = [key for key in game_data.keys() if "factories" in key]
                    for k in factories:
                        game_data[k] += 1
        
        if market_events.time_for_event():
            event = market_events.pick_event()
            if event:
                print(event.text)
                eventsystem.update_game_data(event, game_data)

        produce(game_data)

if __name__=="__main__":
    add_factory(game_data, "mask factories")
    main()