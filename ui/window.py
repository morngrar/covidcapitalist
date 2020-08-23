
import pygame
import time

from ui.event import EventBox
from ui import colors
from ui import textwrap
from ui.factory import FactoryBox

class Window:
    def __init__(self, screen, width, height, fontsizes):
        self.screen = screen
        self.width = width
        self.height = height

        self.game_data = None

        self.event_list = []
        self.event_height = height // 11
        self.event_width = width // 5
        self.event_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes["events"]
        )
        self.event_surface = pygame.Surface((self.event_width, height))
        self.event_surface_pos = (width-self.event_width, 0)
        self.event_xpos = self.event_surface_pos[0]
        self.oldest_event = None

        # width of left part of screen
        self.left_width = width - self.event_width

        # infobar
        self.info_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes["info"]
        )
        self.infobar_height = height // 29
        self.info_pad = (self.infobar_height - fontsizes["info"]) // 2
        self.infobar_surface = pygame.Surface((self.left_width, self.infobar_height))
        renown_width = self.left_width // 4
        self.infobar_renown_rect = pygame.Rect(self.info_pad, self.info_pad, renown_width, self.infobar_height)
        self.infobar_cash_rect = pygame.Rect(
            (
                renown_width,
                self.info_pad, 
                self.left_width - (self.left_width // 4),
                self.infobar_height
            )
        )

        # stock area
        

        # production area
        self.production_height = (height - self.infobar_height) // 2
        self.production_ypos = self.production_height
        self.production_surface = pygame.Surface((self.left_width, self.production_height))
        
        self.mask_factory = FactoryBox(
            self.production_surface, 
            (self.left_width // 3, self.production_height // 3), 
            "Mask Factories", 
            self.info_font, 
            pos=(0, 0)
            )
        
        self.glove_factory = FactoryBox(self.production_surface, (self.left_width // 3, self.production_height // 3), "Glove Factories", self.info_font, pos=(0, self.production_height // 3))
        self.antibac_factory = FactoryBox(self.production_surface, (self.left_width // 3, self.production_height // 3), "Antibac Factories", self.info_font, pos=(0, (self.production_height // 3) * 2 ))
        self.visir_factory = FactoryBox(self.production_surface, (self.left_width // 3, self.production_height // 3), "Visir Factories", self.info_font, pos=(self.left_width // 3, 0))
        self.ventilator_factory = FactoryBox(self.production_surface, (self.left_width // 3, self.production_height // 3), "Ventilator Factories", self.info_font, pos=(self.left_width // 3, self.production_height // 3))
        self.toilet_paper_factory = FactoryBox(self.production_surface, (self.left_width // 3, self.production_height // 3), "Toilet paper Factories", self.info_font, pos=(self.left_width // 3, (self.production_height // 3) * 2 ))

    def add_event(self, event):
        self.event_list.append(
            EventBox(
                self.event_surface,
                (self.event_width, self.event_height),
                event,
                self.event_font
            )
        )
    
    def pop_event(self):
        """Removes oldest event and blacks event area"""
        self.event_list = self.event_list[1:]
        self.event_surface.fill(colors.DARKER_GRAY)

    def update_gamedata(self, data):
        self.game_data = data


    def draw(self):
        # remove oldest event if old
        if self.event_list:
            if time.time() - self.event_list[0].created > 3:
                self.pop_event()

        self.event_surface.fill(colors.DARKER_GRAY)

        # Add event area at right edge of screen
        for i in range(len(self.event_list)):
            if i > 10: # max 10 events on screen
                break
            self.event_list[i].pos = (0, self.event_height*i)
            self.event_list[i].draw()
        self.screen.blit(self.event_surface, self.event_surface_pos)

        # info bar
        self.infobar_surface.fill(colors.DARK_GRAY)
        if not self.game_data:
            renown = "Renown: 50%"
            cash = "Cash: $1000"
        else:
            renown = f"Renown: {self.game_data['renown']}%"
            cash = f"Cash: ${self.game_data['cash']}"

        textwrap.draw_text(
            self.infobar_surface, 
            renown,
            colors.WHITE,
            self.infobar_renown_rect,
            self.info_font,
        )

        textwrap.draw_text(
            self.infobar_surface, 
            cash,
            colors.WHITE,
            self.infobar_cash_rect,
            self.info_font,
        )
        self.screen.blit(self.infobar_surface, (0, 0))

        # Production Area
        # Mask
        self.mask_factory.production = self.game_data["mask factories"] * self.production_rate["mask factories"]
        self.mask_factory.cost = self.production_cost["mask factories"]
        self.mask_factory.draw()
        
        # Glove
        self.glove_factory.production = self.game_data["glove factories"] * self.production_rate["glove factories"]
        self.glove_factory.cost = self.production_cost["glove factories"]
        self.glove_factory.draw()
        
        # Antibac
        self.antibac_factory.production = self.game_data["antibac factories"] * self.production_rate["antibac factories"]
        self.antibac_factory.cost = self.production_cost["antibac factories"]
        self.antibac_factory.draw()

        # Visir
        self.visir_factory.production = self.game_data["visir factories"] * self.production_rate["visir factories"]
        self.visir_factory.cost = self.production_cost["visir factories"]
        self.visir_factory.draw()

        # Ventilator
        self.ventilator_factory.production = self.game_data["ventilator factories"] * self.production_rate["ventilator factories"]
        self.ventilator_factory.cost = self.production_cost["ventilator factories"]
        self.ventilator_factory.draw()

        # Toilet paper
        self.toilet_paper_factory.production = self.game_data["toilet-paper factories"] * self.production_rate["toilet-paper factories"]
        self.toilet_paper_factory.cost = self.production_cost["toilet-paper factories"]
        self.toilet_paper_factory.draw()

        # Blit
        self.screen.blit(self.production_surface, (0, self.production_ypos))

    def update_production_data(self, cost, rate):
        self.production_cost = cost
        self.production_rate = rate