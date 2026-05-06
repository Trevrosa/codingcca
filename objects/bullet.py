import pygame
from pygame.math import Vector2 as vec

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