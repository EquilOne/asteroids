import pygame
import pygame.freetype

default_font = pygame.freetype.get_default_font()

class HUDElement(pygame.sprite.Sprite):
    def __init__(self, default_font, x, y):
        self.position = pygame.Vector2(x, y)
        self.font = pygame.freetype.SysFont(default_font, 20)
        self.color = #FFFFFF

    def draw(self):
    def update(self,)

class Score(HUDElement):
    def __init__(self, default_font, x, y, text, anchor):
        super().__init__(default_font, x, y)


    # def update():
