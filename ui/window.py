
import pygame
import time

from ui.event import EventBox
from ui import colors
from ui import textwrap

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
                renown_width,                               # X
                self.info_pad,                              # Y
                self.left_width - (self.left_width // 4),   # Width
                self.infobar_height                         # Height
            )
        )

        # Stock area
        self.stock_height = (self.height - self.infobar_height) // 2
        self.stock_width = self.left_width

        self.stock_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes['stock']
        )
        self.stock_title_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes['title']
        )
        
        self.stock_surface = pygame.Surface((self.stock_width, self.stock_height))
        self.stock_title_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.left_width, self.infobar_height * 2
        )

        # Mask stock
        self.stock_mask_height = (self.height - self.stock_height) // 6
        self.stock_mask_width = self.left_width // 4
        self.stock_mask_surface = pygame.Surface((self.stock_mask_width, self.stock_mask_height))
        self.stock_mask_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        # Mask demand
        self.demand_mask_height = (self.height - self.stock_height) // 6
        self.demand_mask_width = self.left_width // 4
        self.demand_mask_surface = pygame.Surface((self.stock_mask_width, self.stock_mask_height))
        self.demand_mask_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        # antibac stock
        self.stock_antibac_height = (self.height - self.stock_height) // 6
        self.stock_antibac_width = self.left_width // 4
        self.stock_antibac_surface = pygame.Surface((self.stock_antibac_width, self.stock_antibac_height))
        self.stock_antibac_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        # antibac demand
        self.demand_antibac_height = (self.height - self.stock_height) // 6
        self.demand_antibac_width = self.left_width // 4
        self.demand_antibac_surface = pygame.Surface((self.stock_antibac_width, self.stock_antibac_height))
        self.demand_antibac_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.stock_mask_width, self.infobar_height
        )
        

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


        # Stock box
        self.stock_surface.fill(colors.DARKER_GRAY)
        stockTitle = "WAREHOUSE STOCK"
        textwrap.draw_text(
            self.stock_surface,
            stockTitle,
            colors.WHITE,
            self.stock_title_rect,
            self.stock_title_font,
        )

        # Mask stock
        self.stock_mask_surface.fill(colors.DARK_GRAY)
        stockMask = f"Masks: {self.game_data['mask stock']}"
        textwrap.draw_text(
            self.stock_mask_surface,
            stockMask,
            colors.WHITE,
            self.stock_mask_rect,
            self.stock_font
        )

        # Mask demand
        self.demand_mask_surface.fill(colors.DARK_GRAY)
        demandMask = f"Demand: {self.game_data['mask demand']}"    # Number of demand for
        if self.game_data['mask stock'] < self.game_data['mask demand']: # Check if stock is lower than demand
            demandColor = colors.DARK_RED
        else:
            demandColor = colors.MONEY_GREEN
        
        textwrap.draw_text(
            self.demand_mask_surface,
            demandMask,
            demandColor,
            self.demand_mask_rect,
            self.stock_font
        )
        
        # antibac stock
        self.stock_antibac_surface.fill(colors.DARK_GRAY)
        stockAntibac = f"Antibac: {self.game_data['antibac stock']}"
        textwrap.draw_text(
            self.stock_antibac_surface,
            stockAntibac,
            colors.WHITE,
            self.stock_antibac_rect,
            self.stock_font
        )

        # Mask demand
        self.demand_antibac_surface.fill(colors.DARK_GRAY)
        demandAntibac = f"Demand: {self.game_data['antibac demand']}"    # Number of demand for
        if self.game_data['mask stock'] < self.game_data['mask demand']: # Check if stock is lower than demand
            demandColor = colors.DARK_RED
        else:
            demandColor = colors.MONEY_GREEN
        
        textwrap.draw_text(
            self.demand_mask_surface,
            demandMask,
            demandColor,
            self.demand_mask_rect,
            self.stock_font
        )

        self.screen.blit(self.stock_surface, (0, self.infobar_height)) # Warehouse
        self.screen.blit(self.stock_mask_surface, (self.infobar_height, self.infobar_height * 2))   # Mask stock
        self.screen.blit(self.demand_mask_surface, (self.infobar_height, self.infobar_height * 4))  # Mask demand
        
        