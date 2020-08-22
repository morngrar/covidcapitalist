import pygame

class Widget:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.surface = pygame.Surface(rect.width, rect.height)

    def draw(self, surface, pos):
        surface.blit(self.surface, pos)