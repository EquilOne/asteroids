import os
import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import DEFAULT_FONT, LazyDimensions
from hud import HUDElement
from logger import log_event, log_state
from player import Player
from shot import Shot

screen = None


def main():
    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    os.environ["SDL_VIDEODRIVER"] = "wayland"
    pygame.init()
    # flags = pygame.RESIZABLE
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_rect = screen.get_rect()
    screen_width = LazyDimensions().get_width()
    screen_height = LazyDimensions().get_height()
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
    # score = HUDElement()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        text_surface, text_rect = DEFAULT_FONT.render("Score: 0", "white")
        text_rect.topright = (
            screen_rect.right - HUDElement.PADDING,
            screen_rect.top + HUDElement.PADDING,
        )
        screen.blit(text_surface, text_rect)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            if asteroid.collides_with(asteroid):
                asteroid.split()
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
