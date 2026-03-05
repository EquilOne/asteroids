import pygame
import pygame.freetype

from constants import LazyFont

default_font = LazyFont(24)


class HUDElement(pygame.sprite.Sprite):
    PADDING = 20

    def __init__(self, position, font=default_font):
        self.font = font
        self.color = "#FFFFFF"


class Score(HUDElement):
    SCORE = 0

    def __init__(self):
        pass
