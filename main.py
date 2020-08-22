import pygame

from hello import hello, event_glob_test
from warehouse import checkWarehouse, increaseDemand
from eventsystem import EventStream

# global variables
market_events = EventStream()
game_data = {
    "renown" : 50,
    "cash" : 1000,

    #stock
    "mask stock" : 0,
    "glove stock" : 0,
    "antibac stock" : 0,
    "visir stock" : 0,
    "ventilator stock" : 0,
    "toilet-paper stock" : 1,


    #demand
    "mask demand" : 10,
    "glove demand" : 10,
    "antibac demand" : 10,
    "visir demand" : 10,
    "ventilator demand" : 10,
    "toilet-paper demand" : 1,


    #price
    "mask price" : 5,
    "glove price" : 5,
    "antibac price" : 25,
    "visir price" : 10,
    "ventilator price" : 300,
    "toilet-paper price" : 10,


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

    increaseDemand(game_data)

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

    main()