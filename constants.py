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


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
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
SCORE = 0
DEFAULT_FONT = LazyFont(32)
