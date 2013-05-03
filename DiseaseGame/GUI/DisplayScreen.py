#=====================================================================================
# Filename: DisplayScreen.py
# Author: Ian Zhang
# Description: This file defines a class that is used to display all everything in the screen. 
#               
#=====================================================================================

import pygame
from GUI import Colors


class DisplayScreen(object):
    """Defines some properties of the screen"""

    Resolution = ( 1360, 700 )

    DisplaySurface = pygame.display.set_mode( Resolution, 0, 32)

    def __init__( self ):
        pygame.display.set_caption('Drawing')
        DisplaySurface.fill(Colors.White)                       # Make the background White