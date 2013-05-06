#=====================================================================================
# Filename: GameObject.py
# Author: Ian Zhang
# Description: This file defines GameObject classes, 
#               which is the base class for all visible game objects in the screen.
#=====================================================================================

class GameObject(object):
    """Base Class of all visible objects in the scene"""

    def __init__( self ):
        """
        Constructor
        """
        pass

    def Render(self):
        """
        Render the object in the screen
        """
        pass

    def Update( self, elapsedTime ):
        """
        Update the state of the game object
        """
        pass
