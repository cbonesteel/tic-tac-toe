import sys
import pygame
from colors import *
from settings import *


"""

The application's main method. Contains the main game loop.

"""
def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode(size=(window_width, window_height), flags=pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption('Tic-Tac-Toe')
    clock = pygame.time.Clock()
    done = False

    screen.fill(black)

    while not done:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.update()

    pygame.quit()

"""

Runs the application.

"""
if __name__ == '__main__':
    main()
