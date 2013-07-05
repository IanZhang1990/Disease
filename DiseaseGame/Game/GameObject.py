#=====================================================================================
# Filename: GameObject.py
# Author: Ian Zhang
# Description: This file defines GameObject classes, 
#               which is the base class for all visible game objects in the screen.
#=====================================================================================

from Math.Vector import Vector2D

class GameObject(object):
    """Base Class of all visible objects in the scene"""

    def __init__( self, position, radius, max_speed = None, heading = None, mass = None, scale = 1.0, turn_rate = 1.0, max_force = Vector2D( 0, 0 )  ):
        """
        Constructor
        """
        self.__tag = False
        self.Scale = Vector2D( 1.0, 1.0 )
        self.BoundingRadius = 0
        self.Pos = Vector2D( 0, 0 )
        self.Heading = Vector2D( 0, 0 )
        self.MaxTurnRate = 1.0
        self.Mass = 1.0


        if position is not None and isinstance( position, Vector2D ):
            self.Pos = position
        if heading is not None and isinstance( heading, Vector2D ):
            self.Heading = heading
        if radius is not None:
            self.BoundingRadius = radius
        if max_speed is not None:
            self.MaxSpeed = max_speed
        if mass is not None:
            self.Mass = mass
        if scale is not None :
            self.Scale = scale
        if turn_rate is not None:
            self.MaxTurnRate = turn_rate
        if max_force is not None:
            self.MaxForce = max_force

        self.Side = self.Heading.perpendicular()

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
        self.__tag = False
        pass
    def IsTagged( self ):
        return self.__tag

class ObjectFunctionTemplate:
    
    @staticmethod
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

