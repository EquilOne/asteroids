from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        self.velocity = super().velocity
        self.center = (x, y)
        self.radius = radius

        def draw(self, center, radius):
            pygame.draw.circle(screen, "white", center, self.radius)

        def update(self, dt):
            move_straight = self.position + (self.velocity * dt)
            self.position = move_straight
