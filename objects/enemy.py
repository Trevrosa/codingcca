import pygame
from pygame.math import Vector2 as vec

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], size=30):
        super().__init__()
        self.size = size
        self.pos = vec(pos) - vec(0, self.size)

        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill((255, 0, 200))
        self.rect = self.surf.get_rect(topleft=self.pos)