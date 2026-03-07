import pygame
import pygame.freetype

from constants import LazyFont

PADDING = 20
default_font = LazyFont(24)


class HUDElement(pygame.sprite.Sprite):
    PADDING = 20

    def __init__(self, screen_rect, anchor="topleft", font=default_font):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.screen_rect = screen_rect
        self.anchor = anchor
        self.font = font
        self.color = "#FFFFFF"
        self.text = ""

    def draw(self, screen):
        if not self.text:
            return
        text_surface, text_rect = self.font.render(self.text, self.color)
        screen_anchor = getattr(self.screen_rect, self.anchor)
        if "left" in self.anchor:
            x = screen_anchor[0] + self.PADDING
        else:
            x = screen_anchor[0] - self.PADDING
        if "top" in self.anchor:
            y = screen_anchor[1] + self.PADDING
        else:
            y = screen_anchor[1] - self.PADDING
        setattr(text_rect, self.anchor, (x, y))
        screen.blit(text_surface, text_rect)

    def update(self, dt):
        pass


class Score(HUDElement):
    def __init__(self, screen_rect):
        super().__init__(screen_rect, anchor="topleft")
        self.score = 0

    def update(self, dt):
        self.text = f"Score: {self.score}"
