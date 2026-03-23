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

from consts import WIDTH, HEIGHT, ACCEL, FRICTION, FPS
from util import text

DEBUG = True

pygame.init()
vec = pygame.math.Vector2  # 2 dimensional

frames_per_second = pygame.time.Clock()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")  # you can change this


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))  # rgb
        self.rect = self.surf.get_rect()

        self.initial_pos = vec(15, HEIGHT - 50)
        self.pos = self.initial_pos
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

        if self.pos.y > HEIGHT:
            self.pos = vec(30, HEIGHT - 50)

        # top left align
        if self.pos.x < self.surf.get_width() / 2:
            self.pos.x = self.surf.get_width() / 2
            self.vel.x = 0
        if self.pos.y < self.surf.get_height():
            self.pos.y = self.surf.get_height()
            self.vel.y = 0

        self.rect.midbottom = self.pos

    def jump(self):
        self.vel.y = -15

    # FIXME: might not work if player is on multiple platforms at once
    # FIXME: dont teleport the player if they collide with the side of a platform
    def update(self):
        #                               sprite  sprites  delete?
        hits = pygame.sprite.spritecollide(PLAYER, platforms, False)
        if hits:
            if self.pos.y > hits[0].rect.bottom:
                self.pos.y = (
                    hits[0].rect.bottom
                    + hits[0].surf.get_height()
                    + self.surf.get_height() / 2
                    + 1
                )
                self.vel.y = 0
            else:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], length=WIDTH / 4, width=20):
        super().__init__()

        self.length = length
        self.width = width
        self.pos = vec(pos[0], pos[1] - self.width)

        self.surf = pygame.Surface((self.length, self.width))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(topleft=self.pos)


PLAYER = Player()

platforms = pygame.sprite.Group(
    [
        Platform((0, HEIGHT)),
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
        Platform((WIDTH // 4 - 20, HEIGHT - 190), length=100),
    ]
)

all_sprites = pygame.sprite.Group()
all_sprites.add(PLAYER)
all_sprites.add(platforms)

# only horizontal
CAMERA = PLAYER.initial_pos.x - WIDTH // 2

entity_info = False
grid_lines = True


def transform(pos):
    """turn world coordinates into screen coordinates"""
    cam = max(0, CAMERA)
    if isinstance(pos, vec):
        return pos - vec(cam, 0)
    if isinstance(pos, pygame.Rect):
        return pos.topleft - vec(cam, 0)
    return pos - cam


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
                    entity_info = not entity_info
                elif event.key == K_x:
                    grid_lines = not grid_lines

    display.fill((0, 0, 0))

    PLAYER.move()
    PLAYER.update()

    CAMERA += (PLAYER.pos.x - CAMERA - WIDTH // 2) * 0.05

    for entity in all_sprites:
        display.blit(entity.surf, transform(entity.rect))

    if DEBUG:
        if grid_lines:
            for x in range(0, WIDTH, 20):
                pygame.draw.line(display, (0, 120, 20), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, 20):
                pygame.draw.line(display, (0, 120, 20), (0, y), (WIDTH, y))

            for x in range(0, WIDTH, 60):
                pygame.draw.line(display, (0, 20, 170), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, 60):
                pygame.draw.line(display, (0, 20, 170), (0, y), (WIDTH, y))

        p_pos = text(
            f"pos: ({PLAYER.pos.x:.2f}, {PLAYER.pos.y:.2f}) scr({transform(PLAYER.pos.x):.2f})",
        )
        display.blit(p_pos, (10, 10))

        p_vel = text(f"vel: ({PLAYER.vel.x:.2f}, {PLAYER.vel.y:.2f})")
        display.blit(p_vel, (10, 30))

        cam = text(f"cam: {CAMERA:.2f}")
        display.blit(cam, (10, 50))

        collision = pygame.sprite.spritecollide(PLAYER, platforms, False)
        if collision:
            collision_text = text(
                f"on: {collision[0].pos} scr({transform(collision[0].pos.x):.2f}), l:{collision[0].length} w:{collision[0].width}",
            )
            display.blit(collision_text, (10, 70))

        cursor_pos = vec(pygame.mouse.get_pos())
        cursor = text(f"{cursor_pos} scr({transform(cursor_pos.x):.2f})")
        display.blit(cursor, (cursor_pos.x + 1, cursor_pos.y - 15))

        for entity in all_sprites:
            if entity == PLAYER:
                continue

            info = f"> {entity.pos} scr({transform(entity.pos.x):.2f}), l:{entity.length} w:{entity.width}"
            info = text(info)
            if entity_info:
                display.blit(info, transform(vec(entity.pos.x, entity.pos.y - 15)))
            else:
                cursor = pygame.Rect((cursor_pos.x, cursor_pos.y - 10), (20, 20))

                if cursor.colliderect(entity.rect):
                    display.blit(info, (cursor_pos.x + 1, cursor_pos.y - 15))

    pygame.display.update()
    frames_per_second.tick(FPS)
