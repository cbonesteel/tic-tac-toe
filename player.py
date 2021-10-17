import pygame
from pygame.locals import *
from mark import *
from enum import Enum

class playerType(Enum):
    AI = 0
    HUMAN = 1

class Player():

    """
    
    The player class keeps track of the players moves.

    Parameters:
        screen: The current screen used in the game.
        player: The number of the player, either 1 or 2.
    
    """
    def __init__(self, screen, player, playerType):
        self.moves = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ]
        self.player = player
        self.playerType = playerType
        self.screen = screen
        
        if player == 1:
            self.markType = MarkType.X
        else:
            self.markType = MarkType.O

    """

    Places a mark for the player. Immediately checks for a win condition.

    Parameters:
        position: The position on the board for the mark to go.
    
    Returns:
        Boolean: True if the new marks causes a win.

    """
    def placeMark(self, position):
        x = int(position % 3)
        y = int(position / 3)

        self.moves[x][y] = 1

        newMark = Mark(self.screen, position, self.markType) 
        
        return self.checkWin()
    

    """
    
    Checks to see if the player wins on the current board.
    
    Returns:
        Boolean: True if they have won.

    """
    def checkWin(self):
        for i in range(3):
            sum = 0
            for j in range(3):
                sum += self.moves[i][j]
            if sum == 3:
                return True

        for i in range(3):
            sum = 0
            for j in range(3):
                sum += self.moves[j][i]
            if sum == 3:
                return True

        sum = self.moves[0][0] + self.moves[1][1] + self.moves[2][2]
        if sum == 3:
            return True

        sum = self.moves[0][2] + self.moves[1][1] + self.moves[2][0]
        if sum == 3:
            return True

        return False

    """

    Gets the player type of the player.

    Returns:
        playerType: The type of player.

    """
    def getType(self):
        return self.playerType

    """

    Returns the player's number.

    Returns:
        int: The player's number, either 1 or 2.

    """
    def getNumber(self):
        return self.player
