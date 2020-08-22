import pygame

from hello import hello


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
    main()