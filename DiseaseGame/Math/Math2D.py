


from copy import copy
import math
from Math.Matrix import Matrix3x3
from Math.Vector import Vector2D

class Math2D(object):
    """Math for a 2D area"""

    def __init__(self):
        pass

    @staticmethod
    def WrapAround( posVect2d, maxX, maxY ):
        """reats a window as a toroid"""
        if posVect2d.x > maxX: 
            posVect2d.x = 0.0
        if posVect2d.x < 0:
            posVect2d.x = float(maxX)
        if posVect2d.y > maxY:
            posVect2d.y = 0.0
        if posVect2d.y < 0:
            posVect2d.y = float(maxY)

class Transformations:
    @staticmethod
    def VectorToWorldSpace( vector, agentHeading, agentSide ):
        """Transforms a vector from the agent's local space into world space
        Parameters:
        @vector: Vector2D
        @agentHeading: Vector2D
        @agentSide: Vector2D
        """
        transVect = copy( vector )
        matTrans = Matrix3x3()
        matTrans.Rotate( agentHeading, agentSide )
        matTrans.TransformVector2D( transVect )
        return transVect

    @staticmethod
    def PointToLocalSpace( point, agentHeading, agentSide, agentPosition  ):
        """Transforms a point into the agent's local space.
        Parameters:
        @point: Vector2D
        @agentHeading: Vector2D
        @agentSide: Vector2D
        @agentPosition: Vector2D"""
        transPoint = point
        matTrans = Matrix3x3()
        Tx = - agentPosition.dot( agentHeading )
        Ty = - agentPosition.dot( agentSide )
        # create a transformation matrix
        matTrans.__00 = agentHeading.x
        matTrans.__01 = agentSide.x
        matTrans.__10 = agentHeading.y
        matTrans.__11 = agentSide.y
        matTrans.__20 = Tx
        matTrans.__21 = Ty
        
        # transform the vertices
        matTrans.TransformVector2D( transPoint )
        
        return transPoint 

    @staticmethod
    def VectorToLocalSpace( vector, agentHeading, agentSide ):
        """Transforms a point into the agent's local space.
        Parameters:
        @vector: Vector2D
        @agentHeading: Vector2D
        @agentSide: Vector2D"""

        transPoint = vector
        matTrans = Matrix3x3()
        # create a transformation matrix
        matTrans.__00 = agentHeading.x
        matTrans.__01 = agentSide.x
        matTrans.__10 = agentHeading.y
        matTrans.__11 = agentSide.y
        
        # transform the vertices
        matTrans.TransformVector2D( transPoint )
        
        return transPoint 

    def Vector2DRotateAroundOrigin( vector2d, angle ):
        """rotates a vector ang rads around the origin"""
        if isinstance( vector2d, Vector2D ):
            mat = Matrix3x3()
            mat.Rotate( angle )
            # transform the object's vertices
            mat.TransformVector2D( vector2d )
        else:
            raise TypeError()

