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
import random
from Game.CellSpace import SpacePartition
from Game.GameObject import GameObject
from Utils import ThreadManagement


class GameWorld(object):
    """GameWorld class controls all the basic operations of a game, 
        such as render(), update(), pause(), restart(), restore(), saveGameState()....
    """

    WorldWidth = DisplayScreen.Resolution[0]
    WorldHeight = DisplayScreen.Resolution[1]

    #############################
    ### Game Objects ( GLOBAL )
    #####################################################
    People = list()                       # a container of all avg people
    Doctors = list()                     # a container of all doctors
    Cities = list()                        # a container of all cities
    CellSpace = None                 # Cell SpacePartition.

    ManPath = None                     # any path we may create for the men to follow

    CellsX = 2
    CellsY = 1

    MultiThreadUpdate = True

    def __init__(self):
        self.Pause = False

        border = 30;
        self.ManPath = Path( 8, border, border, GameWorld.WorldWidth-border, GameWorld.WorldHeight-border, True)
        
        # Set up space partitions
        self.CellSpace = SpacePartition( self.WorldWidth, self.WorldHeight, self.CellsX, self.CellsY, 500, self ) # 4 x 3 space partition, with at most 500 agents in it

        self.CellThreadManagement = ThreadManagement.ThreadManager( self.CellSpace )

        # Set up cities

        # Set up roads

        # Set up people 
        manParmLoader = ManParamLoader( "Man.man");
        agentNumber = int(manParmLoader.Parameters.get('AgentNumber', 40))
        steeringParmLoader = SteeringParmLoader( "Steering.str")

        for i in range(0, agentNumber):
            # determine a random starting position
            pos = Vector2D( random.uniform(0, GameWorld.WorldWidth), random.uniform( 0, GameWorld.WorldHeight))
            newPerson = Man.Man( self, manParmLoader, steeringParmLoader, True, 20,  pos, Vector2D(0, 0))
            self.CellSpace.UpdateEntity_NoBlock( newPerson, newPerson.Pos, True )
            self.People.append( newPerson )

    def Render(self):
        """Render objects to the screen"""

        # TODO:
        # I'm not quite sure about this section, but it seems render() method can be called asynchronized, 
        # as long as it is before pygame.draw.update() is called.
        # So... why not try to make this multi-threaded? 

        if not self.Pause:
            for person in self.People:
                    person.Render()
            for doctor in self.Doctors:
                doctor.Render()
            for city in self.Cities:
                city.Render()
            for cell in self.CellSpace.Cells:
                cell.Render()
    
    def TogglePause(self):
        self.Pause = not self.Pause
        pass

    def Update( self, elapsedTime ):
        """Update all the game objects"""
        # TODO:
        # This section has to be implemented by multi-thread ( or even distributed system )
        # Since all game objects are located in a specific cell-space( world is partitioned into several cells  )
        # Each cell can maintain its own status without knowing others, and also, update objects inside it. 
        # Or in other words, each cell can be autonomous

        if not self.Pause:
            if self.MultiThreadUpdate:
                self.CellThreadManagement.Update( elapsedTime )
            else:
                for person in self.People:
                    person.Update( elapsedTime )
            for doctor in self.Doctors:
                doctor.Update( elapsedTime )
            for city in self.Cities:
                city.Update( elapsedTime )
        pass

    def TagEntitiesWithinViewRange( self, entity, range ):
        GameObject.TagNeighbors( entity, self.People, range )
        pass



