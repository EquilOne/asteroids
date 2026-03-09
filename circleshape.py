import pygame

from constants import DEFAULT_COOLDOWN


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.invulnerable = False
        self.invulnerable_cooldown = 0

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass

    def collides_with(self, other):
        if self.position.distance_to(other.position) < (self.radius + other.radius):
            self.invulnerable = True
            other.invulnerable = True
            other.set_invulnerable_cooldown()
            return True
        return False

    def is_invulnerable(self, dt):
        if self.invulnerable_cooldown <= 0:
            self.invulnerable = False
        else:
            self.invulnerable_cooldown -= dt

    def set_invulnerable_cooldown(self):
        self.invulnerable_cooldown = DEFAULT_COOLDOWN
