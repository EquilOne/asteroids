from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = super().velocity
        self.center = (x, y)

        def draw(self, center, radius):
            pygame.draw.circle(screen, "white", center, self.radius, LINE_WIDTH)

        def update(self, dt):
            move_straight = self.position + (self.velocity * dt)
            self.position += move_straight
