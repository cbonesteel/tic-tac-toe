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
            leftX = int(width/25 * (self.positionX + 6 + (4 * self.positionX)))
            rightX = int(width/25 * (self.positionX + 9 + (4 * self.positionX)))
            topY = int(height/25 * (self.positionY + 6 + (4 * self.positionY)))
            botY = int(height/25 * (self.positionY + 9 + (4 * self.positionY)))
            
            pygame.draw.line(self.screen.screen, self.color, (leftX, topY), (rightX, botY), 10)
            pygame.draw.line(self.screen.screen, self.color, (leftX, botY), (rightX, topY), 10)
        else:
            centerX = int(width/10 * (self.positionX + 3 + (1 * self.positionX)))
            centerY = int(height/10 * (self.positionY + 3 + (1 * self.positionY)))
            center = (centerX, centerY)
            
            pygame.draw.circle(self.screen.screen, self.color, center, width/15)
            pygame.draw.circle(self.screen.screen, white, center, width/20)
            
        self.screen.Render()
