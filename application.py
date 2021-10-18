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
    players = []
    players.append(Player(screen, 1, playerType.HUMAN))
    players.append(Player(screen, 2, playerType.HUMAN))

    # Turn counter
    turns = 0

    # Keeps track of used positions
    usedPositions = []

    positions = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        ]
    
    # Main game loop
    while True:
        clock.tick(30)

        currentPlayer = players[turns%2]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and currentPlayer.getType() == playerType.HUMAN:
                win = False
                invalidMove = False
                pos = -1
                
                blockX = window_width / 5
                blockY = window_height / 5
                
                x,y = pygame.mouse.get_pos()
                
                if x < blockX or x > window_width - blockX or y < blockY or y > window_height - blockY:
                    print ("Not a square")
                    invalidMove = True
                else:
                    x = int(x / (blockX)) - 1
                    y = int(y / (blockY)) - 1
                    pos = positions[y][x]

                for i in range(len(usedPositions)):
                    if usedPositions[i] == pos:
                        print("Position in use.")
                        invalidMove = True

                if invalidMove == False:
                    win = currentPlayer.placeMark(pos)
                    usedPositions.append(pos)
                    turns += 1

                if win == True:
                    print(f'Player {currentPlayer.getNumber():1} wins!')

        pygame.display.update()

"""

Runs the application.

"""
if __name__ == '__main__':
    main()
