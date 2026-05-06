from consts import HEIGHT, WIDTH
from objects.platform import Platform
from objects.coin import Coin
from objects.spikes import Spikes

class Level:
    def __init__(self, platforms: list[Platform], coins: list[Coin] = [], spikes: list[Spikes] = []):
        self.platforms = platforms
        self.coins = coins
        self.spikes = spikes

        self.sprites = self.platforms + self.coins + self.spikes

    def remove_coin(self, coin: Coin):
        if coin not in self.coins:
            print("tried to remove coin that does not exist ?")
            return

        print("removing coin at", coin.pos)
        coin.kill()
        self.coins.remove(coin)
        self.sprites.remove(coin)

levels: dict[tuple[int, int], Level] = {}

levels[(0, 0)] = Level(
    platforms=[
        Platform((0, HEIGHT)),
        Platform((WIDTH // 2 - 60, HEIGHT - 70), length=100),
        Platform((WIDTH // 4 - 20, HEIGHT - 190), length=100),
        Platform((WIDTH // 4 - 20 + 100, HEIGHT - 190), length=10, width=100),
        Platform((WIDTH - WIDTH/4, HEIGHT)),        
    ],
    coins=[
        Coin((WIDTH // 2 - 60 + 50, HEIGHT - 70 - 60)),
        Coin((WIDTH // 4 - 20 + 50, HEIGHT - 190 - 60)),
    ],
    spikes=[
        Spikes((WIDTH // 2 - 60 + 50, HEIGHT - 70 - 20)),
        Spikes((WIDTH // 4 - 20 + 50, HEIGHT - 190 - 20)),
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