import pygame
from colors import *
from settings import *

class Screen:

    """

    The screen object that helps generate the window

    """
    def __init__(self):
        self.size = (window_width, window_height)
        self.flags = pygame.SCALED
        self.screen = pygame.display.set_mode(self.size, self.flags)
        self.background = pygame.image.load("resources/menu-background.png")

        pygame.display.set_caption('Tic Tac Toe')

        

    """
    
    Renders an object to the screen.

    Parameters:
        obj (pygame.Surface): The object to be rendered
        pos (Tuple): The position to render the object

    """
    def Render(self, obj=None, pos=None):
        if (obj!=None and pos!=None):
            self.screen.blit(obj,pos)
            pygame.display.update()
        else:
            pygame.display.update()