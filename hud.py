import pygame
import pygame.freetype


class HUD:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.position = pygame.Vector2(x, y)
        self.font = pygame.freetype.getO_default_font()
        self.text = pygame.freetype.SysFont(self.font, 20)

    def write_text(self, screen, input, color):
        self.text.render_to(screen, (self.position.x, self.position.y), input, color)
