import pygame
from ui import textwrap
from ui import colors

BG_COLOR = (50, 50, 50)
BORDER_COLOR = (100, 100, 100)

EVENT_XPAD = 10
EVENT_YPAD = 10


class StockItem:
    """Box which displays a stockitem within the stock box"""
    def __init__(self, surface, dimensions, stockitem, quantity, demand, font, pos=None):
        self.text = stockitem.text
        self.quantity = quantity
        self.demand = demand
        self.surface = surface
        self.font = font
        self.dimensions = dimensions
        self.pos = pos

    def draw(self):
        if not self.pos:
            raise ValueError("Stock item must have position")

        rect = pygame.Rect(self.pos, (self.dimensions))
        inner = pygame.Rect(
            (0, 0, rect.width-EVENT_XPAD, rect.height-EVENT_YPAD)
        )

        inner.clamp_ip(rect)
        inner.x += EVENT_XPAD // 2
        inner.y += EVENT_YPAD // 2

        text_box = pygame.Rect(
            (0, 0, rect.width-EVENT_XPAD*2, rect.height-EVENT_YPAD*2)
        )
        text_box.clamp_ip(rect)
        text_box.x += EVENT_XPAD
        text_box.y += EVENT_YPAD


        pygame.draw.rect(self.surface, BORDER_COLOR, rect)
        pygame.draw.rect(self.surface, BG_COLOR, inner)
        textwrap.draw_text(
            self.surface, 
            self.text, 
            colors.WHITE, 
            text_box,
            self.font,
        )
