#=====================================================================================
from Utils.FileOperation import ParameterLoader
import random
import math
from Utils.Path import Path
from Math.Vector import Vector2D
from Math import Math2D
# Filename: SteeringBehavior.py
# Author: Ian Zhang
# Description: This file defines steering behavior related classes
#=====================================================================================

class SteeringParmLoader( ParameterLoader ):

     def __init__( self, steeringFilename ):
        """Summary:
            Constructor of SteeringParmLoader Class
            Parameters:
            steeringFilename:  The name of the file that defines parameters of steering behavior. It has to be ended with ".str"
        """
        if( str(steeringFilename).endswith('.str') ):
            ParameterLoader.__init__(self, steeringFilename);
            ParameterLoader.LoadFile(self);

class BehaviorType:
    NONE               = 0x00000
    SEEK               = 0x00002
    FLEE               = 0x00004
    ARRIVE             = 0x00008
    WANDER             = 0x00010
    COHESION           = 0x00020
    SEPARATION         = 0x00040
    ALLIGNMENT         = 0x00080
    OBSTACLE_AVOID = 0x00100
    WALL_AVOID     = 0x00200
    FOLLOW_PATH        = 0x00400
    PURSUIT            = 0x00800
    EVADE              = 0x01000
    INTERPOSE          = 0x02000
    HIDE               = 0x04000
    FLOCK              = 0x08000
    OFFSET_PURSUIT     = 0x10000

class SummingMethod:
    WEIGHTED_AVG = 0
    PRIORITIZED = 1
    DITHERED = 2

class SteeringBehavior(object):
    """Steering Behavior"""

    

    def __init__( self, owener, parmLoader ):
        self.Owener = owener
        self.Path = None
        self.SteeringForce = Vector2D(0, 0)

        self.iFlags = 0             # binary flags to indicate whether or not a behavior should be active
        # These can be used to keep track of friends, pursuers, or prey
        self.TargetAgent1 = None
        self.TargetAgent2 = None
        self.Target = None       # The current target

        self.DBoxLength = float(parmLoader.Parameters.get('MinDetectionBoxLength', 40.0))        # length of the 'detection box' utilized in obstacle avoidance
        self.ViewDistance = self.Owener.ViewDistance                                                # how far the agent can 'see'
        self.WanderDistance = 2.0
        self.WanderJitter = 80.0
        self.WanderRadius = 1.2
        self.WanderTarget = None                                                                              # the current position on the wander circle the agent is attempting to steer towards
        self.WaypointSeekDistSq = 400.0                                                                 # the distance (squared) a vehicle has to be from a path waypoint before it starts seeking to the next waypoint
        self.CellSpaceOn = True
        self.SummingMethod = SummingMethod.WEIGHTED_AVG;

        self.WanderWeight = float(parmLoader.Parameters.get('WanderWeight', 1.0))

        # stuff for the wander behavior
        theta = random.uniform(0.0, 1.0) * math.pi * 2.0

        # create a vector to a target position on the wander circle
        self.WanderTarget = Vector2D( self.WanderRadius * math.cos( theta ), self.WanderRadius * math.sin( theta ) )

        # Create a path
        self.Path = Path()
        self.Path.LoopOn()

        # TODO: REMOVE the next line. it is simple for testing.
        self.WanderOn()

######################################################################################
    def Calculate( self ):
        """calculates the accumulated steering force according to the method set in self.SummingMethod"""
        # Reset the steering force
        self.SteeringForce = Vector2D( 0, 0 )

        # use space partitioning to calculate the neighbours of this vehicle
        #if switched on. If not, use the standard tagging system
        if self.CellSpaceOn == False:
            # Tag neighbors
            if self.On( BehaviorType.SEPARATION ) or self.On( BehaviorType.ALLIGNMENT ) or self.On(BehaviorType.COHESION):
                # Tag Neighbors
                self.Owener.World.TagEntitiesWithinViewRange( self.Owener, self.ViewDistance )
        else:
            # calculate neighbours in cell-space
            if self.On( BehaviorType.SEPARATION ) or self.On( BehaviorType.ALLIGNMENT ) or self.On(BehaviorType.COHESION):
                # Tag Neighbors
                self.Owener.World.CellSpace.CalculateNeighbors( self.Owener.Pos, self.ViewDistance )

        if self.SummingMethod == SummingMethod.WEIGHTED_AVG:
            self.SteeringForce = self.CalculateWeightedSum()
        elif self.SummingMethod == SummingMethod.PRIORITIZED:
            self.SteeringForce = self.CalculatePrioritized()
        elif self.SummingMethod == SummingMethod.DITHERED:
            self.SteeringForce = self.CalculateDithered()
        else:
            self.SteeringForce = Vector2D( 0, 0 )
        return self.SteeringForce

    def CalculatePrioritized( self ):
        raise StandardError;

    def CalculateDithered( self ):
        raise StandardError;

    def CalculateWeightedSum( self ):
        """this simply sums up all the active behaviors X their weights and truncates the result to the max available steering force before returning"""
        if self.On( BehaviorType.WALL_AVOID ):
            self.SteeringForce += self.WallAvoidance()
        if self.On( BehaviorType.OBSTACLE_AVOID ):
            self.SteeringForce += self.ObstacleAvoidance()
        if self.On( BehaviorType.EVADE ):
            if self.TargetAgent1 is not None:
                self.SteeringForce += self.Evade()     ##################################### NOT FINISHED IN THIS LINE
        if self.On( BehaviorType.FLEE ):
            # TODO: Flee
                pass

        # The next three can be combined for flocking behavior
        if not self.CellSpaceOn:
            if self.On( BehaviorType.SEPARATION ):
                # TODO: Sepration
                pass
            if self.On( BehaviorType.ALLIGNMENT ):
                # TODO: Allignment
                pass
            if self.On( BehaviorType.COHESION ):
                # TODO: Cohesion
                pass
        else:
            if self.On( BehaviorType.SEPARATION ):
                # TODO: Sepration
                pass
            if self.On( BehaviorType.ALLIGNMENT ):
                # TODO: Allignment
                pass
            if self.On( BehaviorType.COHESION ):
                # TODO: Cohesion
                pass
            pass

        if self.On( BehaviorType.WANDER ):
            self.SteeringForce += self.Wander() * self.WanderWeight
            pass

        # TODO: A lot of things you should do here.
        self.SteeringForce.Truncate( self.Owener.MaxForce )

        return self.SteeringForce


    def WallAvoidance( self ):
        # TODO: FInish the code
        pass
    def ObstacleAvoidance(self):
        # TODO: FInish the code
        pass
    def Evade( self ):
        # TODO: FInish the code
        pass


    def Wander( self ):
        """Man a man wander randomly in the world"""
        # This behavior is dependent on the update rate, so this line must be included when using time independent framerate.
        jitterThisTimeSlice = self.WanderJitter * self.Owener.ElaplsedTime

        # first, add a small random vector to the target's position
        self.WanderTarget += Vector2D( random.uniform( -jitterThisTimeSlice, jitterThisTimeSlice ), random.uniform( -jitterThisTimeSlice, jitterThisTimeSlice ) )

        # reproject this new vector back on to a unit circle
        self.WanderTarget = self.WanderTarget.normalized()

        # increase the length of the vector to the same as the radius of the wander circle
        self.WanderTarget = self.WanderTarget * self.WanderRadius

        # move the target into a position WanderDist in front of the agent

        #normalVect = Vector2D( random.uniform( -2,2 ), random.uniform( -2,2 ) ).normalized()
        target = self.WanderTarget + Vector2D( self.WanderDistance, 0 )

        # project the target into world space
        targetInWorld = Math2D.Transformations.PointToWorldSpace( target, self.Owener.Heading, self.Owener.Side, self.Owener.Pos );

        # and steer towards it
        return targetInWorld - self.Owener.Pos

######################################################################################
    def SetTarget( self, targetPos ):
        self.Target = targetPos

    def SetTargetAgent1( self, agent ):
        self.TargetAgent1 = agent

    def SetTargetAgent2( self, agent ):
        self.TargetAgent2 = agent

    def CreateRandomPath( self, numWayPoints, mx, my, cx, cy ):
        self.Path.CreateRandomPath( numWayPoints, mx, my, cx, cy )

    def ToggleSpacePartition( self ):
            self.CellSpaceOn = not self.CellSpaceOn

    def IsPacePartitionOn( self ):
        return self.CellSpaceOn

    def SetSummingMethod( self, method ):
        self.SummingMethod = method

    def WanderOn( self ):
        self.iFlags = self.iFlags | BehaviorType.WANDER
    def WanderOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.WANDER

    def On( self, behavior ):
        return self.iFlags&behavior == behavior