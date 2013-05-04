#=====================================================================================
# Filename: Path.py
# Author: Ian Zhang
# Description: This file defines path related classes.
#
#=====================================================================================

import math
import random
from Math.Vector import Vector2D
import pygame

def max( a, b ):
    """Return the max value of two nunbers"""
    if a > b:
        return a
    else:
        return b

def min( a, b ):
    """Return the min value of two nunbers"""
    if a < b:
        return a;
    else:
        return b


class Path(object):
    """Define, manage and traverse a path ( defined by a series of 2D vectors )"""

    def __init__( self, numWayPoints=None, minX=None,  minY=None, maxX=None, maxY=None, looped = False ):
        """constructor for creating a path with initial random waypoints. MinX/Y
            & MaxX/Y define the bounding box of the path."""
        self.Looped = looped                       # flag to indicate if the path should be looped
        self.WayPoints = list()                    # (The last waypoint connected to the first)
        self.CurrWayPoint = None                # points to the current waypoint
        self.__currWayPointIndex = 0;       # Index of current way point

        if numWayPoints != None:
            self.CreateRandomPath( numWayPoints, minX, minY, maxX, maxY )
            self.CurrWayPoint = self.WayPoints[0]
            self.__currWayPointIndex = 0;

    def Finished(self):
        return self.CurrWayPoint == self.WayPoints[-1]

    def SetNextWaypoint(self):
        """moves the iterator to the next waypoint in the list"""
        if len(self.WayPoints) > 0:
            if self.CurrWayPoint == self.WayPoints[-2]:
                self.CurrWayPoint = self.WayPoints[0]
            else:
                self.__currWayPointIndex = self.__currWayPointIndex + 1
                self.CurrWayPoint = self.WayPoints[ self.__currWayPointIndex ]

    def LoopOn(self):
        self.Looped = True

    def LoopOff( self ):
        self.Looped = False

    def ToggleLoop( self ):
        if( self.Looped == True ):
            self.Looped = False
        else:
            self.Looped = True

    def AddWayPoint(self, newPoint ):
        """Adds a waypoint to the end of the path"""
        if( type(newPoint) == type( Vector2D ) ):
            self.WayPoints.append( newPoint )

    def Set( self, newPath ):
        """Sets the path with either another Path or a list of vectors"""
        if type( newPath ) == type(self.WayPoints):
            self.WayPoints = newPath
            self.CurrWayPoint = self.WayPoints[0]
            self.__currWayPointIndex = 0
        else:
            if type( newPath ) == type( Path ):
                self.WayPoints = newPath.WayPoints;
                self.CurrWayPoint = self.WayPoints[0]
                self.__currWayPointIndex = 0

    def Clear(self):
        self.WayPoints = list()
        self.CurrWayPoint = None
        self.__currWayPointIndex = 0

    def Render(self, DisplaySurface):
        """Render the Path, NOT IMPLEMENTED YET"""
        print "Path.Render() method is not fully implemented yet."
        #raise Exception()
        Orange = (255, 172, 0)
        pygame.draw.lines( DisplaySurface, Orange, False, self.WayPoints )

    def CreateRandomPath( self, numWayPoints, minX, minY, maxX, maxY ):
        """creates a random path which is bound by rectangle described by the min/max values"""
        self.WayPoints = list()
        
        midX = ( maxX+minX ) / 2.0
        midY = ( minY + maxY ) / 2.0
        smaller = min( midX, midY )
        spacing = math.pi*2.0/numWayPoints

        for i in range(0, numWayPoints):
            RadialDist = random.uniform( smaller * 0.2, smaller )
            temp = Vector2D( RadialDist, 0.0 )
            temp.rotate( i * spacing )
            temp.x += midX
            temp.y += midY

            self.WayPoints.append( temp )

        self.CurrWayPoint = self.WayPoints[0]
        self.__currWayPointIndex = 0;

        return self.WayPoints

