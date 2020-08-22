
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
        INFO_YPAD = 10
        self.info_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes["info"]
        )
        self.infobar_height = height // 19
        self.infobar_surface = pygame.Surface((self.left_width, self.infobar_height))
        infobar_width = self.left_width // 4
        self.infobar_renown_rect = pygame.Rect(0, INFO_YPAD, infobar_width, self.infobar_height)
        self.infobar_cash_rect = pygame.Rect(
            (
                infobar_width,
                INFO_YPAD, 
                self.left_width - (self.left_width // 4),
                self.infobar_height
            )
        )

        # stock area

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

