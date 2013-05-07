#=====================================================================================
# Filename: GameObject.py
# Author: Ian Zhang
# Description: This file defines GameObject classes, 
#               which is the base class for all visible game objects in the screen.
#=====================================================================================

from Math.Vector import Vector2D

class GameObject(object):
    """Base Class of all visible objects in the scene"""

    def __init__( self ):
        """
        Constructor
        """
        self.__tag = False
        self.Scale = Vector2D( 1.0, 1.0 )
        self.BoundingRadius = 0
        self.Pos = Vector2D( 0, 0 )
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

    def Tag(self):
        self.__tag = True
        pass
    def UnTag( self ):
        self.__tag = false
        pass
    def IsTagged( self ):
        return self.__tag

class ObjectFunctionTemplate:
    
    def TagNeighbors( entity, containerOfEntities, radius ):
        """ tags any entities contained in a std container that are within the radius of the single entity parameter"""
        # Iterate through all entities to check for range 
        for curEntity in containerOfEntities:
            # first of all, clear any current tags.
            curEntity.UnTag()

            to = curEntity.Pos - entity.Pos;

            # the bounding radius of the other is taken into account by adding it to the range
            range = radius + curEntity.BoundingRadius

            # if entity within range, tag for further consideration ( working in distance-squard space to avoid sqrts )
            if curEntity != entity and to.get_length_sqrd() < range * range:
                curEntity.Tag()
        pass

