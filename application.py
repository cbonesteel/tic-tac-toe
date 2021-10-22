import sys
import pygame
import pygame_gui
from pygame.locals import *
from colors import *
from settings import *
from board import *
from screen import *
from mark import *
from player import *
from events import *

"""

The application's main method. Contains the main game loop.

"""
def main():
    # Initializes Pygame
    pygame.init()
    manager = pygame_gui.UIManager((window_width, window_height))
    
    # Sets up screen and board
    screen = Screen()
    window_surface = screen.screen
    
    # Sets up clock
    clock = pygame.time.Clock()

    # Creates players
    players = []
    
    # Turn counter
    turns = 0

    # Keeps track of used positions
    usedPositions = []
    
    positions = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        ]

    button_singleplayer = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(window_width / 3, window_width / 3,
     window_width / 3, window_width / 3 / 4), text='Player v. CPU', manager=manager)

    button_multiplayer = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(window_width / 3, window_width / 3 
    + window_width / 3 * .375, window_width / 3, window_width / 3 / 4), text='Player v. Player', manager=manager)

    button_exit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(window_width / 3, window_width / 3 
    + window_width / 3 * .375 * 2, window_width / 3, window_width / 3 / 4), text='Exit', manager=manager)

    game_active = False
    game_init = False
    
    # Main game loop
    while True:
        time_delta = clock.tick(60)/1000.0
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_active == False:            
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == button_singleplayer:
                            players.append(Player(screen, 1, playerType.HUMAN))
                            players.append(Player(screen, 2, playerType.AI))
                            game_active = True
                        elif event.ui_element == button_multiplayer:
                            players.append(Player(screen, 1, playerType.HUMAN))
                            players.append(Player(screen, 2, playerType.HUMAN))
                            game_active = True
                        elif event.ui_element == button_exit:
                            pygame.quit()
                            sys.exit()
                    
                manager.process_events(event)
                manager.update(time_delta)
                manager.draw_ui(window_surface)
                
            if game_active == True:    
                # Builds the board
                if game_init == False:
                    board = Board(screen)
                    game_init = True

                # Handles Turns for Humans
                currentPlayer = players[turns%2]
                win = False
                invalidMove = False

                if event.type == MOUSEBUTTONDOWN and currentPlayer.playerType == playerType.HUMAN:
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
                        pygame.event.post(pygame.event.Event(STARTAI, {}))

                    if win == True:
                        print(f'Player {currentPlayer.player:1} wins!')
                    elif len(usedPositions) == 9:
                        print('Draw')

                # Handles AI
                if event.type == STARTAI and currentPlayer.playerType == playerType.AI:
                    pos = currentPlayer.AIMakeMove(usedPositions)
                    win = currentPlayer.checkWin()
                    usedPositions.append(pos)
                    turns += 1

                    if win == True:
                        print(f'Player {currentPlayer.player:1} wins!')
                    elif len(usedPositions) == 9:
                        print('Draw')

                

        pygame.display.update()

"""

Runs the application.

"""
if __name__ == '__main__':
    main()
