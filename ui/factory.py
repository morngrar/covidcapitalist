import pygame
from ui import textwrap
from ui import colors

BG_COLOR = colors.PRODUCTION_BOX_BG
BORDER_COLOR = (100, 100, 100)
FACTORY_XPAD = 10
FACTORY_YPAD = 10


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
        inner = pygame.Rect(
            (0, 0, rect.width-FACTORY_XPAD, rect.height-FACTORY_YPAD)
        )

        inner.clamp_ip(rect)
        inner.x += FACTORY_XPAD // 2
        inner.y += FACTORY_YPAD // 2

        text_box = pygame.Rect(
            (0, 0, rect.width-FACTORY_XPAD * 2, rect.height-FACTORY_YPAD * 2)
        )

        text_box.clamp_ip(rect)
        text_box.x += FACTORY_XPAD
        text_box.y += FACTORY_YPAD

        row_height = text_box.height // 3
        title_box = pygame.Rect(
            (FACTORY_XPAD, FACTORY_YPAD, text_box.width, row_height)
        )

        production_box = pygame.Rect(
            (FACTORY_XPAD, row_height + FACTORY_YPAD, text_box.width, row_height)
        )

        cost_box = pygame.Rect(
            (FACTORY_XPAD, row_height * 2 + FACTORY_YPAD, text_box.width, row_height)
        )

        pygame.draw.rect(self.surface, colors.WHITE, rect)
        pygame.draw.rect(self.surface, BG_COLOR, inner)

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

