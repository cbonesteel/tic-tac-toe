import sys
import pygame
from pygame.locals import *
from colors import *
from settings import *
from board import *
from screen import *
from mark import *
from player import *

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

    # Creates players
    playerOne = Player(screen, 1, playerType.HUMAN)
    playerTwo = Player(screen, 2, playerType.AI)

    playerOne.placeMark(0)
    playerTwo.placeMark(1)
    
    # Main game loop
    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pressed(num_buttons=3))
                # TODO: Make player place mark based on who's playing
                
        pygame.display.update()

"""

Runs the application.

"""
if __name__ == '__main__':
    main()
