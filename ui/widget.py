import pygame


class Widget:
    def __init__(self, width, height):
        self.surface = pygame.Surface(width, height)
        self.body()

    def draw(self, surface, pos):
        surface.blit(self.surface, pos)

    def body(self):
        pass
