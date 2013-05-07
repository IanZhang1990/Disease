from copy import copy
import math
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
    def PointToWorldSpace( point, agentHeading, agentSide, agentPosition ):
        """Transforms a point from the agent's local space into world space
        Parameters:
        @point: Vector2D
        @agentHeading: Vector2D
        @agentSide: Vector2D
        @agentPosition: Vector2D
        """
        transPoint = copy( point )
        matTrans = 


