import pygame
import pygame.freetype

from constants import DEFAULT_FONT


class HUDElement(pygame.sprite.Sprite):
    PADDING = 20

    def __init__(self, position=(0, 0), font=DEFAULT_FONT):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.font = font
        self.color = "#FFFFFF"
        self.position = pygame.Vector2(position)


class Score(HUDElement):
    score = 0

    def __init__(self):
        super().__init__()

    def update(self, dt):
        pass

    def draw(self, screen):
        text_surface, text_rect = self.font.render(f"Score: {Score.score}", self.color)
        screen_rect = screen.get_rect()
        text_rect.topright = (
            screen_rect.right - self.PADDING,
            screen_rect.top + self.PADDING,
        )
        screen.blit(text_surface, text_rect)
