
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
        
        self.stock_surface = pygame.Surface((self.stock_width,self.stock_height))
        self.stock_title_rect = pygame.Rect(
            self.info_pad, self.info_pad, self.left_width, self.infobar_height * 2
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

        # Stock box
        self.stock_surface.fill(colors.DARKER_GRAY)
        
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

        stockTitle = "WAREHOUSE STOCK"
        textwrap.draw_text(
            self.stock_surface,
            stockTitle,
            colors.WHITE,
            self.stock_title_rect,
            self.stock_title_font,
        )
        
        self.screen.blit(self.infobar_surface, (0, 0))
        self.screen.blit(self.stock_surface, (0,self.infobar_height))