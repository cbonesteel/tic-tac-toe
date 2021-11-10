import sys
import pygame
import pygame_gui
from pygame.locals import *
from pygame_gui.core import ui_element
from colors import *
from settings import *
from board import *
from screen import *
from mark import *
from player import *
from events import *

class GameType(Enum):
    EMPTY = 0
    SINGLEPLAYER = 1
    MULTIPLAYER = 2

class MenuState(Enum):
    MAIN = 0
    SELECTION = 1
    PAUSE = 2
    END_GAME = 3
    NONE = 4

"""

The application's main method. Contains the main game loop.

"""
def main():
    # Initializes Pygame
    pygame.init()
    
    # Sets up screen and board
    board_screen = Screen()
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

    main_manager = pygame_gui.UIManager((window_width, window_height))
    pause_manager = pygame_gui.UIManager((window_width, window_height))
    win_manager = pygame_gui.UIManager((window_width, window_height))
    selection_manager = pygame_gui.UIManager((window_width, window_height), 'x.json')

    # Main Menu
    button_singleplayer = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(window_width / 3, 
    window_width / 3, window_width / 3, window_width / 3 / 4), text='Player v. CPU', manager=main_manager)

    button_multiplayer = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(window_width / 3, 
    window_width / 3  + window_width / 3 * .375, window_width / 3, window_width / 3 / 4), text='Player v. Player', manager=main_manager)

    button_exit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(window_width / 3, window_width / 3 
    + window_width / 3 * .375 * 2, window_width / 3, window_width / 3 / 4), text='Exit', manager=main_manager)

    title = pygame_gui.elements.UIImage(relative_rect=pygame.Rect(window_width / 6 / 2, window_height / 6 / 4, 
    window_width / 1.2, window_height / 6), image_surface=pygame.image.load("resources/title.png"), manager=main_manager)

    # Selection Screen
    selection_title = pygame_gui.elements.UIImage(relative_rect=pygame.Rect(window_width / 6 / 2, window_height / 6 / 4, 
    window_width / 1.2, window_height / 6), image_surface=pygame.image.load("resources/selection.png"), manager=selection_manager)
    x_image = pygame.image.load("resources/x.png")
    o_image = pygame.image.load("resources/o.png")

    # Pause Menu
    paused_title = pygame_gui.elements.UIImage(relative_rect=pygame.Rect(window_width / 6 * 1.5, window_width / 6 * 1.5,
    window_width / 2, window_width / 6), image_surface=pygame.image.load("resources/paused.png"), manager=pause_manager)

    button_resume = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(window_width / 3, window_width / 3
    + window_width / 3 * .375, window_width / 3, window_width / 3 / 4), text='Resume', manager=pause_manager)

    button_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(window_width / 3, window_width / 3 
    + window_width / 3 * .375 * 2, window_width / 3, window_width / 3 / 4), text='Return to Menu', manager=pause_manager)

    # Results Menu
    p1_win = pygame.image.load("resources/p1-win.png")
    p2_win = pygame.image.load("resources/p2-win.png")
    game_draw = pygame.image.load("resources/draw.png")

    button_again = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(window_width / 3, window_width / 3
    + window_width / 3 * .375, window_width / 3, window_width / 3 / 4), text='Play Again', manager=win_manager)

    button_result_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(window_width / 3, window_width / 3 
    + window_width / 3 * .375 * 2, window_width / 3, window_width / 3 / 4), text='Return to Menu', manager=win_manager)

    game_init = False
    game_type = GameType.EMPTY
    menu_state = MenuState.MAIN
    
    # Main game loop
    while True:
        time_delta = clock.tick(60)/1000.0
                
        for event in pygame.event.get():
            #--- X Quit ---#
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #--- MENU EVENTS ---#
            if event.type == MAIN_MENU:
                menu_state = MenuState.MAIN
                game_type = GameType.EMPTY
            if event.type == SELECTION_MENU:
                menu_state = MenuState.SELECTION
            if event.type == ACTIVATE_GAME:
                menu_state = MenuState.NONE
            if event.type == PAUSE_MENU:
                menu_state = MenuState.PAUSE
            if event.type == END_GAME_MENU:
                game_init = False
                turns = 0
                usedPositions = []
                menu_state = MenuState.END_GAME

            #--- MAIN MENU ---#
            if menu_state == MenuState.MAIN:
                screen.screen.blit(screen.background, (0,0))            
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == button_singleplayer:
                            game_type = GameType.SINGLEPLAYER
                            pygame.event.post(pygame.event.Event(SELECTION_MENU, {}))
                        elif event.ui_element == button_multiplayer:
                            players.append(Player(board_screen, 1, playerType.HUMAN))
                            players.append(Player(board_screen, 2, playerType.HUMAN))
                            game_type = GameType.MULTIPLAYER
                            pygame.event.post(pygame.event.Event(ACTIVATE_GAME, {}))
                        elif event.ui_element == button_exit:
                            pygame.quit()
                            sys.exit()
                    
                main_manager.process_events(event)
                main_manager.update(time_delta)
                main_manager.draw_ui(window_surface)

            #--- SINGLEPLAYER MENU ---#
            if menu_state == MenuState.SELECTION:
                screen.screen.fill(white)
                screen.screen.blit(x_image, (window_width / 5, window_width / 5 * 2))
                screen.screen.blit(o_image, (window_width / 5 * 3, window_width / 5 * 2))

                if event.type == MOUSEBUTTONDOWN:
                    blockX = window_width / 5
                    blockY = window_height / 5
                    
                    x,y = pygame.mouse.get_pos()

                    x = int(x / (blockX)) - 1
                    y = int(y / (blockY)) - 1

                    if x == 0 and y == 1:
                        players.append(Player(board_screen, 1, playerType.HUMAN))
                        players.append(Player(board_screen, 2, playerType.AI))
                        pygame.event.post(pygame.event.Event(ACTIVATE_GAME, {}))
                    elif x == 2 and y == 1:
                        players.append(Player(board_screen, 1, playerType.AI))
                        players.append(Player(board_screen, 2, playerType.HUMAN))
                        pygame.event.post(pygame.event.Event(ACTIVATE_GAME, {}))
                        pygame.event.post(pygame.event.Event(STARTAI, {}))
                
                selection_manager.process_events(event)
                selection_manager.update(time_delta)
                selection_manager.draw_ui(window_surface)

            #--- END GAME EVENT HANDLERS ---#
            if event.type == PLAYER_ONE_WINS:
                screen.screen.blit(p1_win, (window_width / 6 / 2, window_height / 6 / 4))
                pygame.event.post(pygame.event.Event(END_GAME_MENU, {}))
            if event.type == PLAYER_TWO_WINS:
                screen.screen.blit(p2_win, (window_width / 6 / 2, window_height / 6 / 4))
                pygame.event.post(pygame.event.Event(END_GAME_MENU, {}))
            if event.type == DRAW:
                screen.screen.blit(game_draw, (window_width / 6 / 2, window_height / 6 / 4))
                pygame.event.post(pygame.event.Event(END_GAME_MENU, {}))

            #--- END GAME MENU ---#
            if menu_state == MenuState.END_GAME:
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == button_again:
                            if game_type == GameType.SINGLEPLAYER:
                                player1 = players[0].playerType
                                player2 = players[1].playerType
                                players = []
                                players.append(Player(board_screen, 1, player1))
                                players.append(Player(board_screen, 2, player2))
                                pygame.event.post(pygame.event.Event(ACTIVATE_GAME, {}))
                                if player1 == playerType.AI:
                                    pygame.event.post(pygame.event.Event(STARTAI, {}))
                            elif game_type == GameType.MULTIPLAYER:
                                players.append(Player(board_screen, 1, playerType.HUMAN))
                                players.append(Player(board_screen, 2, playerType.HUMAN))
                                pygame.event.post(pygame.event.Event(ACTIVATE_GAME, {}))
                        elif event.ui_element == button_result_quit:
                            pygame.event.post(pygame.event.Event(MAIN_MENU, {}))

                win_manager.process_events(event)
                win_manager.update(time_delta)
                win_manager.draw_ui(window_surface)  
            
            #--- GAME ACTIVE ---#
            if menu_state == MenuState.NONE:    
                # Builds the board
                if game_init == False:
                    board = Board(board_screen)
                    game_init = True

                # Handles Turns for Humans
                currentPlayer = players[turns%2]
                win = False
                invalidMove = False
                if event.type == pygame.KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.event.post(pygame.event.Event(PAUSE_MENU, {}))

                if event.type == UNPAUSED:
                    board.DrawBoard()
                    for mark in players[0].marks:
                        mark.Draw()
                    for mark in players[1].marks:
                        mark.Draw()
                
                if event.type == MOUSEBUTTONDOWN and currentPlayer.playerType == playerType.HUMAN:
                    pos = -1
                    
                    blockX = window_width / 5
                    blockY = window_height / 5
                    
                    x,y = pygame.mouse.get_pos()
                
                    if x < blockX or x > window_width - blockX or y < blockY or y > window_height - blockY:
                        invalidMove = True
                    else:
                        x = int(x / (blockX)) - 1
                        y = int(y / (blockY)) - 1
                        pos = positions[y][x]

                    for i in range(len(usedPositions)):
                        if usedPositions[i] == pos:
                            invalidMove = True

                    if invalidMove == False:
                        win = currentPlayer.placeMark(pos)
                        usedPositions.append(pos)
                        turns += 1
                        pygame.event.post(pygame.event.Event(STARTAI, {}))

                    if win == True:
                        if currentPlayer.player == 1:
                            pygame.event.post(pygame.event.Event(PLAYER_ONE_WINS, {}))
                        else:
                            pygame.event.post(pygame.event.Event(PLAYER_TWO_WINS, {}))
                    elif len(usedPositions) == 9:
                        pygame.event.post(pygame.event.Event(DRAW, {}))

                # Handles AI
                if event.type == STARTAI and currentPlayer.playerType == playerType.AI:
                    pos = currentPlayer.AIMakeMove(usedPositions)
                    win = currentPlayer.checkWin()
                    usedPositions.append(pos)
                    turns += 1

                    if win == True:
                        if currentPlayer.player == 1:
                            pygame.event.post(pygame.event.Event(PLAYER_ONE_WINS, {}))
                        else:
                            pygame.event.post(pygame.event.Event(PLAYER_TWO_WINS, {}))
                    elif len(usedPositions) == 9:
                        pygame.event.post(pygame.event.Event(DRAW, {}))   

            #--- PAUSE MENU ---#
            if menu_state == MenuState.PAUSE:
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == button_resume:
                            pygame.event.post(pygame.event.Event(UNPAUSED, {}))
                            menu_state = MenuState.NONE
                        elif event.ui_element == button_quit:
                            game_init = False
                            players = []
                            turns = 0
                            usedPositions = []
                            game_type = GameType.EMPTY
                            pygame.event.post(pygame.event.Event(MAIN_MENU, {}))

                pause_manager.process_events(event)
                pause_manager.update(time_delta)
                pause_manager.draw_ui(window_surface)      

        pygame.display.update()

"""

Runs the application.

"""
if __name__ == '__main__':
    main()
