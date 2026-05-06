import pygame
from pygame.math import Vector2 as vec

from consts import WIDTH


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], length=WIDTH / 4, width=20):
        super().__init__()

        self.length = length
        self.width = width
        self.pos = vec(pos) - vec(0, self.width)

        self.surf = pygame.Surface((self.length, self.width))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(topleft=self.pos)
