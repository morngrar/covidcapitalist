import pygame
from ui import textwrap
from ui import colors

BG_COLOR = (50, 50, 50)
BORDER_COLOR = (100, 100, 100)


class FactoryBox:
    """Box which displays a factory """
    def __init__(self, surface, dimensions, title, font, pos=None):
        self.title = title
        self.parent_surface = surface
        self.font = font
        self.dimensions = dimensions
        self.pos = pos
        self.surface = pygame.Surface(dimensions)
        self.production = None
        self.cost = None

    def get_rect(self):
        return pygame.Rect(self.pos, self.dimensions)

    def draw(self):
        if not self.pos:
            raise ValueError("Factory must have position")

        rect = pygame.Rect((0, 0), (self.dimensions))
        row_height = rect.height // 3
        title_box = pygame.Rect(
            (0, 0, rect.width, row_height)
        )

        production_box = pygame.Rect(
            (0, row_height, rect.width, row_height)
        )

        cost_box = pygame.Rect(
            (0, row_height * 2, rect.width, row_height)
        )

        pygame.draw.rect(self.surface, BG_COLOR, rect)
        textwrap.draw_text(
            self.surface, 
            self.title, 
            colors.WHITE, 
            title_box,
            self.font,
        )

        textwrap.draw_text(
            self.surface, 
            f"Produces: {self.production}",
            colors.WHITE, 
            production_box,
            self.font,
        )

        textwrap.draw_text(
            self.surface, 
            f"Cost: {self.cost}",
            colors.WHITE, 
            cost_box,
            self.font,
        )

        self.parent_surface.blit(self.surface, self.pos)

