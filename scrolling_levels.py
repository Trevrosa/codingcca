from pygame import Vector2 as vec

from consts import HEIGHT, WIDTH
from objects.platform import Platform
from objects.end import End
from objects.enemy import Enemy
from objects.spikes import Spikes


class Level:
    def __init__(self, start_position, platforms: list[Platform], end: End, enemies: list[Enemy] = [], spikes: list[Spikes] = []):
        self.start_position = vec(start_position)
        self.platforms = platforms
        self.end = end
        self.enemies = enemies
        self.spikes = spikes

        self.sprites = platforms + [end] + enemies + spikes


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
    ],
    spikes=[
        Spikes((WIDTH // 2 - 60 + 50, HEIGHT - 70 - 20)),
        Spikes((WIDTH // 4 - 20 + 50, HEIGHT - 190 - 20)),
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
