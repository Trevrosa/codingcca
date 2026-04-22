import pygame
from pygame.math import Vector2 as vec

from consts import DEBUG


class End(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], size=40):
        super().__init__()

        self.size = size
        self.pos = vec(pos) - vec(0, self.size)

        self.surf = pygame.Surface((self.size, self.size))
        if DEBUG:
            self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(topleft=self.pos)
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], size=30):
        super().__init__()
        self.size = size
        self.pos = vec(pos) - vec(0, self.size)

        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill((255, 0, 200))
        self.rect = self.surf.get_rect(topleft=self.pos)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], vel: vec):
        super().__init__()
        self.vel = vel
        self.pos = vec(pos)

        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect(topleft=self.pos)
    
    def update(self):
        self.pos += self.vel
        self.rect.topleft = self.pos