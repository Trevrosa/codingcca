from consts import HEIGHT, WIDTH
from objects import Platform

class Level:
    def __init__(self, platforms: list[Platform]):
        self.platforms = platforms

        self.sprites = platforms

levels = {}

levels[(0, 0)] = Level(
    platforms=[
        Platform((0, HEIGHT)),
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
        Platform((WIDTH // 4 - 20, HEIGHT - 190), length=100),
        Platform((WIDTH - WIDTH/4, HEIGHT)),
    ]
)

levels[(0, 1)] = Level(
    platforms=[
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
        Platform((WIDTH // 4 - 20, HEIGHT - 190), length=100),
    ]
)

levels[(0, -1)] = Level(
    platforms=[
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
        Platform((WIDTH // 4 - 20, HEIGHT - 190), length=100),
    ]
)

levels[(1, 0)] = Level(
    platforms=[
        Platform((0, HEIGHT)),
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
        Platform((WIDTH - 300, HEIGHT - 100), length=100),
    ]
)

levels[(-1, 0)] = Level(
    platforms=[
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
        Platform((WIDTH - 300, HEIGHT - 100), length=100),
        Platform((WIDTH - WIDTH/4, HEIGHT)),
    ]
)