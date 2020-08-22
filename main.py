import pygame

from hello import hello, event_glob_test
from eventsystem import EventStream
from productionsystem import add_factory

# global variables
market_events = EventStream()
game_data = {
    "renown" : 50,
    "cash" : 1000,

    #stock
    "masks" : 0,
    "gloves" : 0,
    "antibac" : 0,
    "visirs" : 0,
    "ventilators" : 0,
    "toilet paper" : 0,

    # factories
    "mask factories" : 0,
    "glove factories" : 0,
    "antibac factories" : 0,
    "visir factories" : 0,
    "ventilator factories" : 0,
    "tp factories" : 0,


    # off the books production
    "moonshine producers" : 0,
}

def main():
    """The games main loop

    """

    HIDPI = True
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    pygame.init()

    if HIDPI:
        SCREEN_HEIGHT *= 2
        SCREEN_WIDTH *= 2

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption("COVID Capitalist")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__=="__main__":
    hello()
    print(market_events.events)
    event_glob_test(market_events)  # changes global, since python passes by ref
    print(market_events.events)
    add_factory(game_data, "ventilators")
    print(game_data)

    main()