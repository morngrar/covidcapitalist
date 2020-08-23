import time
import pygame
from warehouse import checkWarehouse, increaseDemand
import productionsystem
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
    "mask price" : 5,
    "glove price" : 7,
    "antibac price" : 20,
    "visir price" : 10,
    "ventilator price" : 300,
    "toilet-paper price" : 10,

    # factories
    "mask factories" : 0,
    "glove factories" : 0,
    "antibac factories" : 0,
    "visir factories" : 0,
    "ventilator factories" : 0,
    "toilet-paper factories" : 0,
    "moonshiner factories": 0,
    "childlabor factories": 0,
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

    window.update_production_data(productionsystem.factory_cost, productionsystem.factory_production_rate)

    # music
    import os
    bgmusic = os.path.join("audio", "covid capitalist.ogg")
    factoryshopsound = os.path.join("audio", "8-bit-powerup_01.ogg")
    eventsound = os.path.join("audio", "eventsound.ogg")
    pygame.mixer.init()
    pygame.mixer.music.load(bgmusic)
    pygame.mixer.music.play(-1, 0.0)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # mask factory
                rect = window.mask_factory.get_rect()
                rect = pygame.Rect(rect.x, window.production_ypos + rect.y, rect.width, rect.height)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if productionsystem.add_factory(game_data, "mask factories"):
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound(factoryshopsound))
                    print(pygame.mouse.get_pos())
                
                # glove factory
                rect = window.glove_factory.get_rect()
                rect = pygame.Rect(rect.x, window.production_ypos + rect.y, rect.width, rect.height)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if productionsystem.add_factory(game_data, "glove factories"):
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound(factoryshopsound))
                    print(pygame.mouse.get_pos())

                # antibac factory
                rect = window.antibac_factory.get_rect()
                rect = pygame.Rect(rect.x, window.production_ypos + rect.y, rect.width, rect.height)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if productionsystem.add_factory(game_data, "antibac factories"):
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound(factoryshopsound))
                    print(pygame.mouse.get_pos())

                # visir factory
                rect = window.visir_factory.get_rect()
                rect = pygame.Rect(rect.x, window.production_ypos + rect.y, rect.width, rect.height)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if productionsystem.add_factory(game_data, "visir factories"):
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound(factoryshopsound))
                    print(pygame.mouse.get_pos())

                # ventilator factory
                rect = window.ventilator_factory.get_rect()
                rect = pygame.Rect(rect.x, window.production_ypos + rect.y, rect.width, rect.height)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if productionsystem.add_factory(game_data, "ventilator factories"):
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound(factoryshopsound))
                    print(pygame.mouse.get_pos())

                # toilet-paper factory
                rect = window.toilet_paper_factory.get_rect()
                rect = pygame.Rect(rect.x, window.production_ypos + rect.y, rect.width, rect.height)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if productionsystem.add_factory(game_data, "toilet-paper factories"):
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound(factoryshopsound))
                    print(pygame.mouse.get_pos())

                # moonshiners
                rect = window.offbooks_moonshiners.get_rect()
                rect = pygame.Rect(window.offbooks_xpos + rect.x, window.offbooks_ypos + rect.y, rect.width, rect.height)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    productionsystem.add_factory(game_data, "moonshiner factories")
                    market_events.add(
                        eventsystem.Event(
                            "A documentary revealed one of your moonshiner connections! They had to shut down!",
                            {
                                "renown": -5,
                                "moonshiner factories": -1
                            },
                            oneoff=True
                        )
                    )


                #child labor
                rect = window.offbooks_child_labor.get_rect()
                rect = pygame.Rect(window.offbooks_xpos + rect.x, window.offbooks_ypos + rect.y, rect.width, rect.height)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    productionsystem.add_factory(game_data, "childlabor factories")
                    market_events.add(
                        eventsystem.Event(
                            "A documentary revealed one of your child labor facilities! It had to be shut down!",
                            {
                                "renown": -10,
                                "childlabor factories": -1
                            },
                            oneoff=True
                        )
                    )

        if market_events.time_for_event():
            event = market_events.pick_event()
            if event:
                if eventsystem.update_game_data(event, game_data):
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound(eventsound))
                    window.add_event(event)

        productionsystem.produce(game_data)


        window.update_gamedata(game_data)
        window.draw()
        pygame.display.update()

if __name__=="__main__":
    main()