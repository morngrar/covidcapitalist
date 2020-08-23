import time
import pygame
from warehouse import checkWarehouse, increaseDemand
from productionsystem import produce
import eventsystem


deltatime = 0
last_time = 0


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

    HIDPI = False
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


    from ui.window import Window
    window = Window(
        screen, 
        SCREEN_WIDTH, 
        SCREEN_HEIGHT,

        # font sizes
        {
            "events":EVENT_FONT_SIZE,
            "info": int(EVENT_FONT_SIZE * 1.8),
            "stock":int(EVENT_FONT_SIZE * 1.6),
            "title":int(EVENT_FONT_SIZE * 2),
        }
    )


    running = True
    while running:
        global deltatime
        global last_time
        now = time.time()
        deltatime += now - last_time
        last_time = now

        # Increase demand and sell stock in intervals
        if deltatime >= 1:
            checkWarehouse(game_data)
        if deltatime >= 2:
            deltatime = 0
            increaseDemand(game_data)               
        
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
                if eventsystem.update_game_data(event, game_data):
                    window.add_event(event)

        produce(game_data)
        window.update_gamedata(game_data)
        window.draw()
        pygame.display.update()

if __name__=="__main__":
    main()