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
from Game.Urban import Building, City
import Game


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
    Buildings = list()                   # All buildings

    ManPath = None                     # any path we may create for the men to follow

    CellsX = 5
    CellsY = 4

    MultiThreadUpdate = False

    def __init__(self):
        self.Pause = False

        #the position of the crosshair
        self.Crosshair = Vector2D( self.WorldWidth / 2.0, self.WorldHeight/2.0 ) 

        border = 30;
        self.ManPath = Path( 8, border, border, GameWorld.WorldWidth-border, GameWorld.WorldHeight-border, True)
        
        # Set up space partitions
        self.CellSpace = SpacePartition( self.WorldWidth, self.WorldHeight, self.CellsX, self.CellsY, 500, self ) # 4 x 3 space partition, with at most 500 agents in it

        if( self.MultiThreadUpdate ):
            self.CellThreadManagement = ThreadManagement.ThreadManager( self.CellSpace )

        # Set up cities
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!########################### 
        #This is for test only
        newCity = City( Vector2D(self.WorldWidth / 2.0, self.WorldHeight / 2.0 ) )
        self.Cities.append( newCity )

        """
        newBuilding = Building( Vector2D(600, 400), 40 )
        newBuilding.IsObstacle = True
        newCity.AddBuilding( newBuilding )
        self.Buildings.append( newBuilding )

        newBuilding2 = Building( Vector2D(300, 400), 50 )
        newBuilding2.IsObstacle = True
        newCity.AddBuilding( newBuilding2 )
        self.Buildings.append( newBuilding2 )

        newBuilding3 = Building( Vector2D(700, 200), 30 )
        newBuilding3.IsObstacle = True
        newCity.AddBuilding( newBuilding3 )
        self.Buildings.append( newBuilding3 )

        newBuilding4 = Building( Vector2D(800, 500), 20 )
        newBuilding4.IsObstacle = True
        newCity.AddBuilding( newBuilding4 )
        self.Buildings.append( newBuilding4 )

        newBuilding5 = Building( Vector2D(1000, 600), 25 )
        newBuilding5.IsObstacle = True
        newCity.AddBuilding( newBuilding5 )
        self.Buildings.append( newBuilding5 )

        newBuilding6 = Building( Vector2D(400, 600), 50 )
        newBuilding6.IsObstacle = True
        newCity.AddBuilding( newBuilding6 )
        self.Buildings.append( newBuilding6 )
        """
        ##############################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! --------------------- End Test 

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
            for city in self.Cities:
                city.Render()
            for cell in self.CellSpace.Cells:
                cell.Render()
            for person in self.People:
                    person.Render()
            for doctor in self.Doctors:
                doctor.Render()
    
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
        Game.GameObject.ObjectFunctionTemplate.TagNeighbors( entity, self.People, range )
        pass

    def TagObstaclesWithinViewRange( self, entity, range ):
        ObstBuilding = list()
        for building in self.Buildings:
            if building.IsObstacle:
                ObstBuilding.append( building )
        Game.GameObject.ObjectFunctionTemplate.TagNeighbors( entity, ObstBuilding, range )
        pass

    def SetCrosshair( self, VectorOrPoints ):
        if isinstance( VectorOrPoints, Vector2D ):
            self.Crosshair = VectorOrPoints
        else:
            pass