#=====================================================================================
# Filename: GameWorld.py
# Author: Ian Zhang
# Description: This file defines GameWorld class, which controls all the basic 
#                  operations of a game.
#
#=====================================================================================

from GUI.DisplayScreen import DisplayScreen
from Utils.Path import Path
from Game.Man import ManParamLoader
from Game import Man
from Utils.SteeringBehavior import SteeringBehavior
from Utils.SteeringBehavior import SteeringParmLoader
from Math.Vector import Vector2D
import math
from random import random

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

    ManPath = None                     # any path we may create for the men to follow

    def __init__(self):

        border = 30;
        self.ManPath = Path( 8, border, border, self.WorldWidth-border, self.WorldHeight-border, True)

        # Set up cities

        # Set up roads

        # Set up people 
        manParmLoader = ManParamLoader( "Man.man");
        agentNumber = int(manParmLoader.Parameters.get('AgentNumber', 40))
        steeringParmLoader = SteeringParmLoader( "Steering.str")

        for i in range(0, agentNumber):
            # determine a random starting position
            pos = Vector2D( random.uniform(0, self.WorldWidth), random.uniform( 0, self.WorldHeight))
            newPerson = Man.Man( self, manParmLoader, steeringParmLoader, True, 20,  pos, Vector2D(0, 0))
            self.People.append( newPerson )

    def Render(self):
        """Render objects to the screen"""
        if not self.Pause:
            for person in self.People:
                person.Render()
            for doctor in self.Doctors:
                doctor.Render()
            for city in self.Cities:
                city.Render()

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

