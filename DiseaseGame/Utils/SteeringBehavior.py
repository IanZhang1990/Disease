#=====================================================================================
from Utils.FileOperation import ParameterLoader
import random
import math
from Utils.Path import Path
from Math.Vector import Vector2D
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
        self.Path = Null
        self.SteeringForce = Vector2D(0, 0)

        self.iFlags = 0             # binary flags to indicate whether or not a behavior should be active
        # These can be used to keep track of friends, pursuers, or prey
        self.TargetAgent1 = Null
        self.TargetAgent2 = Null
        self.Target = Null             # The current target

        self.DBoxLength = parmLoader.Parameters.get('MinDetectionBoxLength')        # length of the 'detection box' utilized in obstacle avoidance
        self.ViewDistance = parmLoader.Parameters.get('ViewDistance');                    # how far the agent can 'see'
        self.WanderDistance = 2.0
        self.WanderJitter = 80.0
        self.WanderRadius = 1.2
        self.WanderTarget = Null                                                                              # the current position on the wander circle the agent is attempting to steer towards
        self.WaypointSeekDistSq = 400.0                                                                 # the distance (squared) a vehicle has to be from a path waypoint before it starts seeking to the next waypoint
        self.CellSpaceOn = True
        self.SummingMethod = SummingMethod.DITHERED;


        # stuff for the wander behavior
        theta = random.uniform(0.0, 1.0) * math.pi * 2.0

        # create a vector to a target position on the wander circle
        self.WanderTarget = Vector2D( self.WanderRadius * math.cos( theta ), self.WanderRadius * math.sin( theta ) )

        # Create a path
        self.Path = Path()
        self.Path.LoopOn()

######################################################################################
    def Calculate( self ):
        """calculates the accumulated steering force according to the method set in self.SummingMethod"""
        # Reset the steering force
        self.SteeringForce.x = 0
        self.SteeringForce.y = 0

        # use space partitioning to calculate the neighbours of this vehicle
        #if switched on. If not, use the standard tagging system
        if self.CellSpaceOn == False:
            # Tag neighbors
            if On( BehaviorType.SEPARATION ) or On( BehaviorType.ALLIGNMENT ) or On(BehaviorType.COHESION):
                # Tag Neighbors
                raise Exception();
        else:
            # calculate neighbours in cell-space
            if On( BehaviorType.SEPARATION ) or On( BehaviorType.ALLIGNMENT ) or On(BehaviorType.COHESION):
                # Tag Neighbors
                raise Exception();

    def Wander( self ):
        """Man a man wander randomly in the world"""
        # This behavior is dependent on the update rate, so this line must be included when using time independent framerate.
        jitterThisTimeSlice = self.WanderJitter * self.Owener.ElaplsedTime

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