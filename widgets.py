""" Widgets are drawable objects in the game """

import pygame


class Widget:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.surface.fill((80, 80, 80))

    def draw(self, surface, pos):
        surface.blit(self.surface, pos)


class Factorywidget(Widget): 
    def __init__(self, rect):
        super().__init__(rect)
