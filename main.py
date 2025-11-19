import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def main():
    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")

    while True:
        log_state()
        screen.fill("black")
        pygame.display.flip()


if __name__ == "__main__":
    main()
