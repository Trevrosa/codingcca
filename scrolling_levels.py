import sys
from pygame import Vector2 as vec

from consts import HEIGHT, WIDTH
from objects import End, Platform


class Level:
    def __init__(self, start_position, platforms: list[Platform], end: End):
        self.start_position = vec(start_position)
        self.platforms = platforms
        self.end = end

        self.sprites = platforms + [end]


level1 = Level(
    start_position=(15, HEIGHT - 30),
    platforms=[
        Platform((0, HEIGHT)),
        Platform((WIDTH // 4 - 20, HEIGHT - 190), length=100),
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
    ],
    end=End((WIDTH // 2 + 10, HEIGHT - 90)),
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

# Get all Level instances from the current module
current_module = sys.modules[__name__]
levels = [
    getattr(current_module, name)
    for name in dir(current_module)
    if isinstance(getattr(current_module, name), Level) and name.startswith("level")
]
