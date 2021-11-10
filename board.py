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
        self.screen.screen.fill(self.color)
        
        self.screen.Render(obj=self,pos=(0,0))

        (width, height) = self.screen.size
        
        pygame.draw.line(self.screen.screen, black, (width/5 * 2, height/5), (width/5 * 2,height/5 * 4), 5)

        pygame.draw.line(self.screen.screen, black, (width/5 * 3, height/5), (width/5 * 3,height/5 * 4), 5)

        pygame.draw.line(self.screen.screen, black, (width/5, height/5 * 2), (width/5 * 4,height/5 * 2), 5)

        pygame.draw.line(self.screen.screen, black, (width/5, height/5 * 3), (width/5 * 4,height/5 * 3), 5)
        
        self.screen.Render()
