import pygame

from colors import *

class Board(pygame.Surface):

    """
    
    The board class sets up the graphical display of the board. It displays Xs 
    and Os also known as marks inside of the board.

    Parameters:
        screen: The screen to draw the board on. This will be the main screen found in application.

    """
    def __init__(self, screen):
        self.screen = screen
        self.color = white

        super().__init__(self.screen.size)
        self.convert()
        self.fill(white)

        self.DrawBoard()

    """

    Draw the board to the screen.

    """
    def DrawBoard(self):
        self.fill(self.color)

        self.screen.Render(obj=self,pos=(0,0))

        pygame.draw.rect(self.screen.screen, black, pygame.Rect(1,1,10,10), 0)

        self.screen.Render()
