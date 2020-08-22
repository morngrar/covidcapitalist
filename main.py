import pygame

import eventsystem

# global variables
market_events = eventsystem.EventStream()
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

    # demand
    "masks demand" : 0,
    "gloves demand" : 0,
    "antibac demand" : 0,
    "visirs demand" : 0,
    "ventilators demand" : 0,
    "toilet-paper demand" : 0,

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

    from textwraptest import drawText
    font = pygame.font.Font('freesansbold.ttf', EVENT_FONT_SIZE)
    text_box = (50, 100, 200, 500)
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(text_box))
    drawText(screen, "Testing drawing some text", (255,255,255), text_box, font)
    pygame.display.update()

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


if __name__=="__main__":
    main()