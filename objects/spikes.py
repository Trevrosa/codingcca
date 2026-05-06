import pygame
from pygame.math import Vector2 as vec


class Spikes(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float]):
        super().__init__()
        self.pos = vec(pos) - vec(0, 5) # so it sticks out of the platform

        self.surf = pygame.Surface((20, 15)) # x y
        self.surf.fill((128, 128, 128))  # grey
        self.rect = self.surf.get_rect(topleft=self.pos)
