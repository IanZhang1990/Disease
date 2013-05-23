#=====================================================================================
from Math.Vector import Vector2D
import pygame
from GUI.DisplayScreen import DisplayScreen
from GUI.Colors import Colors
# Filename: Vector.py
# Author: Ian Zhang
# Description: This is a 2D vector class, has operator overloading (can use with tuples or lists), 
#               uses slots for perforance, is picklable, implements list interface (so it's compatible 
#               with pygame functions), has a fair bit of high level vector operators (for performance 
#               and readability)
#=====================================================================================

class InvertedAABBox2D(object):
    """simple inverted (y increases down screen) axis aligned bounding box class"""

    def __init__(self, topLeftVec2d, bottomRightVec2d):
        self.TopLeft = topLeftVec2d
        self.BottomRight = bottomRightVec2d
        self.Center = Vector2D( (self.TopLeft.x+self.BottomRight.x)/2.0, (self.TopLeft.y+self.BottomRight.y)/2.0 )

    def Top(self):
        return self.TopLeft.y

    def Bottom( self ):
        return self.BottomRight.y

    def Left( self ):
        return self.TopLeft.x

    def Right( self ):
        return self.BottomRight.x

    def IsOverlapWith( self, AABBox ):
        """returns true if another bbox intersects with this one"""
        return not( AABBox.Top() > self.Bottom() 
                     or AABBox.Bottom() < self.Top()
                     or AABBox.Left() > self.Right()
                     or AABBox.Right() < self.Left() )

    def Render(self):
        lines = [ (self.Left(),  self.Top()), (self.Right(), self.Top()), (self.Right(), self.Bottom()), (self.Left(),self.Bottom()), (self.Left(),  self.Top()) ]
        pygame.draw.lines( DisplayScreen.DisplaySurface, Colors.BlueViolet, False, lines )