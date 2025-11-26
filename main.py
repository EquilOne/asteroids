import sys

import pygame
import pygame.freetype

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from hud import write_text
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
    asteroid_field = AsteroidField()
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        write_text(screen, "testing", "white")
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
