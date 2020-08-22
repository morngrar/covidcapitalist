import pygame
from ui import textwrap
from ui import colors

BG_COLOR = (50, 50, 50)
BORDER_COLOR = (100, 100, 100)


class FactoryBox:
    """Box which displays a factory """
    def __init__(self, surface, dimensions, title, font, pos=None):
        self.title = title
        self.surface = surface
        self.font = font
        self.dimensions = dimensions
        self.pos = pos

    def draw(self):
        if not self.pos:
            raise ValueError("Event must have position")

        rect = pygame.Rect(self.pos, (self.dimensions))
        inner = pygame.Rect(
            (0, 0, rect.width, rect.height)
        )

        text_box = pygame.Rect(
            (0, 0, rect.width, rect.height)
        )

        pygame.draw.rect(self.surface, BORDER_COLOR, rect)
        pygame.draw.rect(self.surface, BG_COLOR, inner)
        textwrap.draw_text(
            self.surface, 
            self.title, 
            colors.WHITE, 
            text_box,
            self.font,
        )
