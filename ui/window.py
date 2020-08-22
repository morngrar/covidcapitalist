
import pygame
import time

from ui.event import EventBox
from ui import colors

class Window:
    def __init__(self, screen, width, height, fontsizes):
        self.screen = screen
        self.width = width
        self.height = height

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

        # stock area
        self.stock_height = (height - (height//19)) // 2
        self.stock_width = width - self.event_width
        self.stock_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes['stock']
        )
        self.stock_surface = pygame.Surface(self.stock_width, self.stock_height)
        self.stock_pos = (height + (height//19), 0)

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
        self.event_surface.fill(colors.BLACK)

    def draw(self):
        # remove oldest event if old
        if self.event_list:
            if time.time() - self.event_list[0].created > 3:
                self.pop_event()

        # Add event area at right edge of screen
        for i in range(len(self.event_list)):
            if i > 10: # max 10 events on screen
                break
            self.event_list[i].pos = (0, self.event_height*i)
            self.event_list[i].draw()

        self.screen.blit(self.event_surface, self.event_surface_pos)
        self.screen.blit(self.stock_surface, self.stock_surface_pos)



