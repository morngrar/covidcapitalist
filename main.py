import pygame

from hello import hello, event_glob_test
from eventsystem import EventStream

# global event variable
market_events = EventStream()

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

    main()