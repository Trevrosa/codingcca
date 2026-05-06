import pygame
from pygame.math import Vector2 as vec

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float]):
        super().__init__()

        self.pos = vec(pos)

        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect(topleft=self.pos)