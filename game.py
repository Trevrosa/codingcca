import sys
import pygame
from pygame.constants import (
    K_c,
    K_x,
    K_z,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    KMOD_CTRL,
    QUIT,
    KEYDOWN,
)
from pygame.math import Vector2 as vec

from consts import DEBUG, WIDTH, HEIGHT, ACCEL, FRICTION, FPS
from objects.platform import Platform
from util import debug

pygame.init()

frames_per_second = pygame.time.Clock()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")  # you can change this


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))  # rgb
        self.rect = self.surf.get_rect()

        self.pos = vec(15, HEIGHT - 50)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

    def move(self):
        self.accel = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.accel.x = -ACCEL
        if pressed_keys[K_RIGHT]:
            self.accel.x = ACCEL

        self.accel.x += self.vel.x * -FRICTION
        self.vel += self.accel
        self.pos += self.vel + 0.5 * self.accel

        self.rect.midbottom = self.pos  # type: ignore

    def jump(self):
        self.vel.y = -15

    # FIXME: dont teleport the player if they collide with the side of a platform
    def update(self):
        #                               sprite  sprites  delete?
        hits = pygame.sprite.spritecollide(PLAYER, LEVEL, False)  # type: ignore
        for hit in hits:
            if self.pos.y > hit.rect.bottom:
                self.pos.y = (
                    hits[0].rect.bottom
                    + hits[0].surf.get_height()
                    + self.surf.get_height() / 2
                    + 1
                )  # fmt: skip
                self.vel.y = 0
            else:
                self.pos.y = hit.rect.top + 1
                self.vel.y = 0

        if self.pos.x > WIDTH - self.surf.get_width() / 2 or self.pos.y > HEIGHT:
            self.pos = vec(15, HEIGHT - 50)

        # top left align
        if self.pos.x < self.surf.get_width() / 2:
            self.pos.x = self.surf.get_width() / 2
            self.vel.x = 0
        if self.pos.y < self.surf.get_height():
            self.pos.y = self.surf.get_height()
            self.vel.y = 0


PLAYER = Player()

LEVEL = pygame.sprite.Group(
    [
        Platform((0, HEIGHT)),
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
        Platform((WIDTH // 4 - 20, HEIGHT - 190), length=100),
    ]  # type: ignore
)

ALL_SPRITES = pygame.sprite.Group()
ALL_SPRITES.add(PLAYER)
ALL_SPRITES.add(LEVEL)

show_entity_info = False
show_grid_lines = True

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                PLAYER.jump()
            elif event.mod & KMOD_CTRL and event.key == K_c:
                pygame.quit()
                sys.exit()
            elif DEBUG:
                if event.key == K_z:
                    show_entity_info = not show_entity_info
                elif event.key == K_x:
                    show_grid_lines = not show_grid_lines

    display.fill((0, 0, 0))

    PLAYER.move()
    PLAYER.update()

    for entity in ALL_SPRITES:
        display.blit(entity.surf, entity.rect)

    if DEBUG:
        debug(
            display,
            PLAYER,
            ALL_SPRITES,
            LEVEL,
            show_grid_lines,
            show_entity_info,
        )

    pygame.display.update()
    frames_per_second.tick(FPS)
