import pygame

from eventsystem import EventStream

# global variables
market_events = EventStream()
game_data = {
    "renown" : 50,
    "cash" : 1000,

    #stock
    "masks stock" : 0,
    "gloves stock" : 0,
    "antibac stock" : 0,
    "visirs stock" : 0,
    "ventilators stock" : 0,
    "toilet-paper stock" : 0,

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
    """The games main loop"""

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
    main()