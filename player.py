import pygame
from pygame import cursors
from pygame.draw import circle
from pygame.locals import *
from pygame.surfarray import array2d
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
        self.marks = []
        
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
        x = int(position / 3)
        y = int(position % 3)

        self.moves[x][y] = 1

        newMark = Mark(self.screen, position, self.markType) 
        
        self.marks.append(newMark)
        
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
    
    Handles AI decision making process.

    Parameters:
        usedPositions: An array of the used positions of the complete game.
    
    """
    def AIMakeMove(self, usedPositions):
        positions = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        ]

        currentBoard = []
        # Creates an array to analyze based on the current board state
        for i in range(3):
            currentBoard.append([])
            for j in range(3):
                currentBoard[i].append(self.moves[i][j])
        
        # Adds other player's positons
        for i in range(len(usedPositions)):
            x = int(usedPositions[i] / 3)
            y = int(usedPositions[i] % 3)
            if currentBoard[x][y] == 0:
                currentBoard[x][y] = 2
        
        movePlayed = False
        for i in range(8):
            if i == 0:
                movePlayed, pos = self.canWin(currentBoard, positions)
            elif i == 1:
                movePlayed, pos = self.canBlock(currentBoard, positions)
            elif i == 2:
                movePlayed, pos = self.canFork(currentBoard, positions)
            elif i == 3:
                movePlayed, pos = self.blockFork(currentBoard, positions)
            elif i == 4:
                movePlayed, pos = self.playCenter(currentBoard, positions)
            elif i == 5:
                movePlayed, pos = self.playOpCorner(currentBoard, positions)
            elif i == 6:
                movePlayed, pos = self.playCorner(currentBoard, positions)
            elif i == 7:
                movePlayed, pos = self.playSide(currentBoard, positions)

            if movePlayed == True:
                break

        return pos

    """
    
    Checks to see if the opposing player wins on a new move.

    Parameters:
        currentBoard: A 2D array representing the current game board.
    
    Returns:
        Boolean: True if they have won.

    """
    def checkOpWin(self, currentBoard):
        for i in range(3):
            sum = 0
            for j in range(3):
                sum += currentBoard[i][j]
            if sum == 6:
                return True

        for i in range(3):
            sum = 0
            for j in range(3):
                sum += currentBoard[j][i]
            if sum == 6:
                return True

        sum = currentBoard[0][0] + currentBoard[1][1] + currentBoard[2][2]
        if sum == 6:
            return True

        sum = currentBoard[0][2] + currentBoard[1][1] + currentBoard[2][0]
        if sum == 6:
            return True

        return False

    """

    Counts the number of wins currently possible on the board for the opponent.

    Parameters:
        currentBoard: The current board to be checked.

    Returns:
        Int: The current number of possible wins for the opponent on the board.

    """
    def countOpWins(self, currentBoard):
        wins = 0
        for i in range(3):
            sum = 0
            blocked = False
            for j in range(3):
                if currentBoard[i][j] == 1:
                    blocked = True
                else:
                    sum += currentBoard[i][j]
                
            if sum == 4 and not blocked:
                wins += 1


        for i in range(3):
            sum = 0
            blocked = False
            for j in range(3):
                if currentBoard[j][i] == 1:
                    blocked = True
                else:
                    sum += currentBoard[j][i]
                
            if sum == 4 and not blocked:
                wins += 1

        sum = currentBoard[0][0] + currentBoard[1][1] + currentBoard[2][2]
        if sum == 4 and currentBoard[0][0] != 1 and currentBoard[1][1] != 1 and currentBoard[2][2] != 1:
            wins += 1

        sum = currentBoard[0][2] + currentBoard[1][1] + currentBoard[2][0]
        if sum == 4 and currentBoard[0][2] != 1 and currentBoard[1][1] != 1 and currentBoard[2][0] != 1:
            wins += 1

        return wins

    """

    Counts the number of wins currently possible on the board.

    Parameters:
        currentBoard: The current board to be checked.

    Returns:
        Int: The current number of possible wins on the board.

    """
    def countWins(self, currentBoard):
        wins = 0
        for i in range(3):
            sum = 0
            blocked = False
            for j in range(3):
                if currentBoard[i][j] == 2:
                    blocked = True
                else:
                    sum += self.moves[i][j]
                
            if sum == 2 and not blocked:
                wins += 1


        for i in range(3):
            sum = 0
            blocked = False
            for j in range(3):
                if currentBoard[j][i] == 2:
                    blocked = True
                else:
                    sum += self.moves[j][i]
                
            if sum == 2 and not blocked:
                wins += 1

        sum = self.moves[0][0] + self.moves[1][1] + self.moves[2][2]
        if sum == 2 and currentBoard[0][0] != 2 and currentBoard[1][1] != 2 and currentBoard[2][2] != 2:
            wins += 1

        sum = self.moves[0][2] + self.moves[1][1] + self.moves[2][0]
        if sum == 2 and currentBoard[0][2] != 2 and currentBoard[1][1] != 2 and currentBoard[2][0] != 2:
            wins += 1

        return wins
        
    """

    Checks if there is a postion that will lead to a win.

    Parameters:
        currentBoard: A 2D array defining the current board.
        positions: A 2D array labeling the positions on a 0 - 8 scale.

    Returns:
        Boolean: True if a move was made, false otherwise

    """
    def canWin(self, currentBoard, positions):
        win = False

        for i in range(3):
            for j in range(3):
                if currentBoard[i][j] == 0:
                    self.moves[i][j] = 1
                    win = self.checkWin()
                    self.moves[i][j] = 0
                if win == True:
                    self.placeMark(positions[i][j])
                    return True, positions[i][j]
        
        return False, -1

    """

    Checks to see if there is an empty position that would lead to the opponent winning.

    Parameters:
        currentBoard: A 2D array defining the current board.
        positions: A 2D array labeling the positions on a 0 - 8 scale.

    Returns:
        Boolean: True if a move was made, false otherwise

    """
    def canBlock(self, currentBoard, positions):
        win = False

        for i in range(3):
            for j in range(3):
                if currentBoard[i][j] == 0:
                    currentBoard[i][j] = 2
                    win = self.checkOpWin(currentBoard)
                    currentBoard[i][j] = 0
                if win == True:
                    self.placeMark(positions[i][j])
                    return True, positions[i][j]
        
        return False, -1

    """

    Checks to see if there is an empty position that would lead to the creation
    of 2 winning conditions for the AI.

    Parameters:
        currentBoard: A 2D array defining the current board.
        positions: A 2D array labeling the positions on a 0 - 8 scale.

    Returns:
        Boolean: True if a move was made, false otherwise

    """
    def canFork(self, currentBoard, positions):
        turn = 0
        winsPossible = 0
        played = False
        for i in range(3):
            for j in range(3):
                turn += self.moves[i][j]

        if turn == 0 and self.player == 1:
            return self.playCorner(currentBoard, positions)
        elif turn == 0:
            played, position = self.playCenter(currentBoard, positions)
            if played == True:
                return played, position
            else:
                return self.playCorner(currentBoard, positions)

        
        if turn == 1 and self.player == 1:
            if currentBoard[2][2] == 0:
                self.placeMark(positions[2][2])
                return True, positions[2][2]
            elif currentBoard[0][2] == 0:
                self.placeMark(positions[0][2])
                return True, positions[0][2]
            elif currentBoard[2][0] == 0:
                self.placeMark(positions[2][0]) 
                return True, positions[2][0]
        
        for i in range(3):
            for j in range(3):
                if currentBoard[i][j] == 0:
                    self.moves[i][j] = 1
                    winsPossible = self.countWins(currentBoard)
                    self.moves[i][j] = 0
                if winsPossible >= 2:
                    self.placeMark(positions[i][j])
                    return True, positions[i][j]

        return False, -1  

    """

    Checks to see if there is an empty position that would lead to the opponent creating
    two winning conditions for himself.

    Parameters:
        currentBoard: A 2D array defining the current board.
        positions: A 2D array labeling the positions on a 0 - 8 scale.

    Returns:
        Boolean: True if a move was made, false otherwise

    """
    def blockFork(self, currentBoard, positions):
        winsPossible = 0
        for i in range(3):
            for j in range(3):
                if currentBoard[i][j] == 0:
                    currentBoard[i][j] = 2
                    for k in range(3):
                        for l in range(3):
                            if currentBoard[k][l] == 0:
                                currentBoard[k][l] = 2
                                winsPossible = self.countOpWins(currentBoard)
                                currentBoard[k][l] = 0
                    currentBoard[i][j] = 0
                    if winsPossible >= 2:
                        self.placeMark(positions[i][j])
                        return True, positions[i][j]

        return False, -1

    """

    Checks to see if the center is empty.

    Parameters:
        currentBoard: A 2D array defining the current board.
        positions: A 2D array labeling the positions on a 0 - 8 scale.

    Returns:
        Boolean: True if a move was made, false otherwise

    """
    def playCenter(self, currentBoard, positions):
        if currentBoard[1][1] == 0:
            self.placeMark(positions[1][1])
            return True, positions[1][1]

        return False, -1

    """

    Checks to see if there is an empty corner opposite of the other player's
    move.

    Parameters:
        currentBoard: A 2D array defining the current board.
        positions: A 2D array labeling the positions on a 0 - 8 scale.

    Returns:
        Boolean: True if a move was made, false otherwise

    """
    def playOpCorner(self, currentBoard, positions):
        if currentBoard[0][0] == 2 and currentBoard[2][2] == 0:
            self.placeMark(positions[2][2])
            return True, positions[2][2]
        elif currentBoard[0][2] == 2 and currentBoard[2][0] == 0:
            self.placeMark(positions[2][0])
            return True, positions[2][0]
        elif currentBoard[2][0] == 2 and currentBoard[0][2] == 0:
            self.placeMark(positions[0][2])
            return True, positions[0][2]
        elif currentBoard[2][2] == 2 and currentBoard[0][0] == 0:
            self.placeMark(positions[0][0])
            return True, positions[0][0]
        else:
            return False, -1

    """

    Checks to see if there is an empty corner to play in.

    Parameters:
        currentBoard: A 2D array defining the current board.
        positions: A 2D array labeling the positions on a 0 - 8 scale.

    Returns:
        Boolean: True if a move was made, false otherwise

    """
    def playCorner(self, currentBoard, positions):
        if currentBoard[0][0] == 0:
            self.placeMark(positions[0][0])
            return True, positions[0][0]
        elif currentBoard[0][2] == 0:
            self.placeMark(positions[0][2])
            return True, positions[0][2]
        elif currentBoard[2][0] == 0:
            self.placeMark(positions[2][0])
            return True, positions[2][0]
        elif currentBoard[2][2] == 0:
            self.placeMark(positions[2][2])
            return True, positions[2][2]
        else:
            return False, -1

    """

    Checks to see if there is an empty side to play in.

    Parameters:
        currentBoard: A 2D array defining the current board.
        positions: A 2D array labeling the positions on a 0 - 8 scale.

    Returns:
        Boolean: True if a move was made, false otherwise

    """
    def playSide(self, currentBoard, positions):
        if currentBoard[0][1] == 0:
            self.placeMark(positions[0][1])
            return True, positions[0][1]
        elif currentBoard[1][0] == 0:
            self.placeMark(positions[1][0])
            return True, positions[1][0]
        elif currentBoard[1][2] == 0:
            self.placeMark(positions[1][2])
            return True, positions[1][2]
        elif currentBoard[2][1] == 0:
            self.placeMark(positions[2][1])
            return True, positions[2][1]
        else:
            return False, -1