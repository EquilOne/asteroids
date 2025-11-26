import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        # new_vector_1 = self.velocity.rotate(random_angle)
        # new_vector_2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_1.velocity = self.velocity.rotate(random_angle) * 1.2
        new_asteroid_2.velocity = self.velocity.rotate(-random_angle) * 1.2

    def update(self, dt):
        move_straight = self.velocity * dt
        self.position += move_straight
