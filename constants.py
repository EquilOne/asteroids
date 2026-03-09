import pygame
import pygame.freetype


class LazyFont:
    def __init__(self, size):
        self.size = size
        self._font = None

    def _get_font(self):
        if self._font is None:
            self._font = pygame.freetype.Font(None, self.size)
        return self._font

    def __getattr__(self, name):
        return getattr(self._get_font(), name)

    def __get__(self, obj, objtype=None):
        return self


class LazyDimensions:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self._width = None
        self._height = None

    def get_width(self):
        if self._width is None:
            self._width = self.screen.get_width()
        return self._width

    def get_height(self):
        if self._height is None:
            self._height = self.screen.get_height()
        return self._height


PLAYER_RADIUS = 20
LINE_WIDTH = 2
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_SPAWN_RATE_SECONDS = 0.8
PLAYER_SHOOT_SPEED = 500
SHOT_RADIUS = 5
PLAYER_SHOT_COOLDOWN_SECONDS = 0.3
DEFAULT_COOLDOWN = 1.5
DEFAULT_FONT = LazyFont(24)
