#=====================================================================================
# Filename: GameWorld.py
# Author: Ian Zhang
# Description: This file defines GameWorld class, which controls all the basic 
#                  operations of a game.
#
#=====================================================================================

from GUI.DisplayScreen import DisplayScreen

class GameWorld(object):
    """GameWorld class controls all the basic operations of a game, 
        such as render(), update(), pause(), restart(), restore(), saveGameState()....
    """

    WorldWidth = DisplayScreen.Resolution[0]
    WorldHeight = DisplayScreen.Resolution[1]
    Pause = False

    #############################
    ### Game Objects
    #####################################################
    People = list()                       # a container of all avg people
    Doctors = list()                     # a container of all doctors
    Cities = list()                        # a container of all cities

    ManPath = Null                     # any path we may create for the men to follow

    def __init__(self):
        pass

    def Render(self):
        """Render objects to the screen"""
        if not self.Pause:
            for person in self.People:
                person.Update( elapsedTime )
            for doctor in self.Doctors:
                doctor.Update( elapsedTime )
            for city in self.Cities:
                city.Update( elapsedTime )

            # Render everything
            raise Exception();
    
    def Pause(self):
        self.Pause = not self.Pause


    def Update( self, elapsedTime ):
        """Update all the game objects"""
        for person in self.People:
            person.Update( elapsedTime )
        for doctor in self.Doctors:
            doctor.Update( elapsedTime )
        for city in self.Cities:
            city.Update( elapsedTime )

