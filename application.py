import sys
import pygame
from colors import *
from settings import *
from board import *
from screen import *

"""

The application's main method. Contains the main game loop.

"""
def main():
    # Initializes Pygame
    pygame.init()

    # Sets up screen and board
    screen = Screen()
    board = Board(screen)

    # Sets up clock
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

"""

Runs the application.

"""
if __name__ == '__main__':
    main()
