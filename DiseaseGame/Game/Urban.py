


from Game import GameObject
from Math.Vector import Vector2D
from GUI.Colors import Colors
import pygame
from GUI.DisplayScreen import DisplayScreen

class City(GameObject.GameObject):
    """description of class"""
    def __init__( self, centerPosition ):
        self.CenterPos = centerPosition
        self.Buildings = list()
        pass
    def AddBuilding( self, building ):
        self.Buildings.append( building )
    
    def Render( self ):
        for building in self.Buildings:
            building.Render()
        pass

    def Update( self, timeElapsed ):
        pass

class BuildingType:
    CIRCLE = 0

class Building( GameObject.GameObject ):
    """description of class"""
    def __init__( self, position, size = 40 ):
        self.Size = size
        self.Pos = position
        self.IsObstacle = True
        pass

    def Update( self, timeElapsed ):
        pass

    def Render( self ):
        drawingColor = None
        if self.IsObstacle:
            drawingColor = Colors.Black
        else:
            drawingColor = Colors.Gray
            pass
        posX = int( self.Pos.x )
        posY = int(self.Pos.y)
        pygame.draw.circle( DisplayScreen.DisplaySurface, drawingColor, ( posX, posY ), int(self.Size) )       




class Highway( Building ):
    """description of class"""



class Hospital( Building ):
    """description of class"""

