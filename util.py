from consts import FONT

from pygame.font import Font
from pygame.surface import Surface


def text(text: str, font: Font = FONT) -> Surface:
    """renders text to a surface with a black background and white text"""
    return font.render(
        text,
        True,
        (255, 255, 255),
        (0, 0, 0),
    )
