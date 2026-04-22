from pygame import Vector2 as vec

from consts import HEIGHT, WIDTH
from objects import Platform
from scrolling_objects import End, Enemy


class Level:
    def __init__(self, start_position, platforms: list[Platform], end: End, enemies: list[Enemy] = []):
        self.start_position = vec(start_position)
        self.platforms = platforms
        self.end = end
        self.enemies = enemies

        self.sprites = platforms + [end] + enemies


level1 = Level(
    start_position=(15, HEIGHT - 30),
    platforms=[
        Platform((0, HEIGHT)),
        Platform((WIDTH // 4 - 20, HEIGHT - 190), length=100),
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
    ],
    end=End((WIDTH // 2 + 10, HEIGHT - 90)),
    enemies=[
        Enemy((WIDTH // 2 + 100, HEIGHT - 100)),
    ]
)

level2 = Level(
    start_position=(15, 0),
    platforms=[
        Platform((0, HEIGHT)),
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
        Platform((WIDTH - 300, HEIGHT - 100), length=100),
    ],
    end=End((WIDTH // 2 + 300, HEIGHT - 90)),
)

levels = [x for x in list(vars().values()) if isinstance(x, Level)]
