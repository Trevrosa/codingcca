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
from grid_levels import levels
from objects.coin import Coin
from objects.spikes import Spikes
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

        self.score = 0

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

    def update(self):
        global level_pos
        #                               sprite  sprites  delete?
        hits = pygame.sprite.spritecollide(PLAYER, LEVEL, False)  # type: ignore
        for hit in hits:
            if isinstance(hit, Coin):
                levels[level_pos].remove_coin(hit)
                self.score += 1
                continue
            if isinstance(hit, Spikes):
                level_pos = (0, 0)
                self.vel = vec(0, 0)
                self.pos = vec(15, HEIGHT - 50)
                setup_level()
                continue
            if self.pos.x < hit.rect.left:
                self.pos.x = hit.rect.left - self.surf.get_width() / 2
                self.vel.x = 0
            elif self.pos.x > hit.rect.right:
                self.pos.x = hit.rect.right + self.surf.get_width() / 2
                self.vel.x = 0
            elif self.pos.y > hit.rect.bottom:
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

        if self.pos.x > WIDTH - self.surf.get_width() / 2:
            level_pos = (level_pos[0] + 1, level_pos[1])
            self.pos = vec(self.surf.get_width() / 2, self.pos.y)
            setup_level()
        
        if self.pos.y > HEIGHT:
            level_pos = (level_pos[0], level_pos[1] - 1)
            self.pos = vec(self.pos.x, self.surf.get_height())
            setup_level()

        if self.pos.x < self.surf.get_width() / 2:
            level_pos = (level_pos[0] - 1, level_pos[1])
            self.pos = vec(WIDTH - self.surf.get_width() / 2, self.pos.y)
            setup_level()
            
        if self.pos.y < self.surf.get_height():
            level_pos = (level_pos[0], level_pos[1] + 1)
            self.pos = vec(self.pos.x, HEIGHT - self.surf.get_height())
            setup_level()


PLAYER = Player()

level_pos = (0, 0)
LEVEL = pygame.sprite.Group(levels[level_pos].sprites)

ALL_SPRITES = pygame.sprite.Group()
ALL_SPRITES.add(PLAYER)
ALL_SPRITES.add(LEVEL)

show_entity_info = False
show_grid_lines = True

def setup_level():
    global LEVEL, level_pos
    
    if level_pos not in levels:
        print(f"WARN: going to (0, 0) because tried to goto level {level_pos} which does not exist")
        level_pos = (0, 0)
    
    print(f"loading level at {level_pos}")
    
    LEVEL = pygame.sprite.Group(levels[level_pos].sprites)
    
    ALL_SPRITES.empty()
    ALL_SPRITES.add(PLAYER)
    ALL_SPRITES.add(LEVEL)


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
            world_info=f"{level_pos}",
        )

    pygame.display.update()
    frames_per_second.tick(FPS)
