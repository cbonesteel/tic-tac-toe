import pygame
from enum import Enum
from colors import *

class MarkType(Enum):
    O = 0
    X = 1

class Mark:

    """
    
    The mark class draws a new mark to the screen. The mark can be either an X or an O.

    Parameters:
        screen: The screen to draw the mark on.
        position: The position on the board to draw the mark.
        markType: The type of mark, either an X or an O.

    """
    def __init__(self, screen, position, markType):
        self.screen = screen
        self.markType = markType

        if self.markType == MarkType.O:
            self.color = red
        else:
            self.color = blue

        self.positionX = int(position % 3)
        self.positionY = int(position / 3)

        self.Draw()

    """

    Draw the mark on the screen.
    
    """
    def Draw(self):

        (width, height) = self.screen.size

        if self.markType == MarkType.X:
            pic = pygame.image.load("resources/x.png")
            x = int(width/25 * (self.positionX + 5 + (4 * self.positionX)))
            y = int(height/25 * (self.positionY + 5 + (4 * self.positionY)))
            self.screen.screen.blit(pic, (x, y))
        else:
            pic = pygame.image.load("resources/o.png")
            x = int(width/25 * (self.positionX + 5 + (4 * self.positionX)))
            y = int(height/25 * (self.positionY + 5 + (4 * self.positionY)))
            self.screen.screen.blit(pic, (x, y))
            
        self.screen.Render()
