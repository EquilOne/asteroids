import os
import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from hud import Counters, HUDElement, Score
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    os.environ["SDL_VIDEODRIVER"] = "wayland"
    pygame.init()
    # flags = pygame.RESIZABLE
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_rect = screen.get_rect()
    screen_width, screen_height = screen_rect.bottomright
    # screen_width = LazyDimensions().get_width()
    # screen_height = LazyDimensions().get_height()
    print(f"Screen width: {screen_width} \nScreen height: {screen_height}")
    clock = pygame.time.Clock()
    dt = 0
    asteroids = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (drawable, shots, updatable)
    Player.containers = (updatable, drawable)
    HUDElement.containers = (drawable, updatable)
    asteroid_field = AsteroidField()
    player = Player(x=screen_rect.centerx, y=screen_rect.centery)
    score = Score(screen_rect)
    counters = Counters(screen_rect)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for asteroid in asteroids:
            if not player.invulnerable and asteroid.collides_with(player):
                player.make_invulnerable()
                log_event("player_hit")
                counters.lives -= 1
                asteroid.split()
                if counters.lives <= 0:
                    print("Game over!")
                    sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    score.score += 5
                    shot.kill()
                    asteroid.split()
                    if asteroid.asteroid_destroyed:
                        score.score += 5
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
