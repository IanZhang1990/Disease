#=====================================================================================
# Filename: SteeringBehavior.py
# Author: Ian Zhang
# Description: This file defines steering behavior related classes
#=====================================================================================
from Utils.FileOperation import ParameterLoader
import random
import math
from Utils.Path import Path
from Math.Vector import Vector2D
from Math import Math2D
from Game import GameObject


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

class ArriveMode:
    """Arrive makes use of these to determine how quickly a vehicle should decelerate to its target"""
    SLOW = 3
    NORMAL = 2
    FAST = 1

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
        #Arrive makes use of these to determine how quickly a vehicle should decelerate to its target
        self.ArriveMode = ArriveMode.NORMAL                                                      # By default, the arrive mode is normal

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
                pass
        else:
            # calculate neighbours in cell-space
            if self.On( BehaviorType.SEPARATION ) or self.On( BehaviorType.ALLIGNMENT ) or self.On(BehaviorType.COHESION):
                # Tag Neighbors
                self.Owener.World.CellSpace.CalculateNeighbors( self.Owener.Pos, self.ViewDistance )
                pass

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


###############################################
###                                Behaviors
############################################### 

    def WallAvoidance( self ):
        # TODO: FInish the code
        pass
    def ObstacleAvoidance(self):
        # TODO: FInish the code
        pass

    def Seek( self, targetPos ):
        """Giving a target the method returns a steering force point towards the target"""
        if not isinstance( targetPos, Vector2D ):
            return
        desireVelo = (targetPos - self.Owener.Pos).normalized() * self.Owener.MaxSpeed
        return desireVelo - self.Owener.Velocity;

    def Flee( self, targetPos ):
        """Giving a target the method returns a steering force point against the target"""
        if not isinstance( targetPos, Vector2D ):
            return
        desireVelo = (self.Owener.Pos - targetPos).normalized() * self.Owener.MaxSpeed
        return desireVelo - self.Owener.Velocity;

    def Evade( self, pursuer ):
        """Flees from the estimated future position of the pursuer"""
        if not isinstance( pursuer, Game.Man.Man ):
            return
        toPursuer = pursuer.Pos - self.Owener.Pos
        ThreadRange = 100.0 #######################################################  TODO: Please make this a parameter
        if toPursuer.get_length_sqrd() > ThreadRange * ThreadRange:
            return Vector2D( 0, 0 )
        
        # the lookahead time is propotional to the distance between the pursuer
        # and the pursuer; and is inversely proportional to the sum of the
        # agents' velocities
        lookAheadTime = toPursuer.get_length() / ( self.Owener.MaxSpeed + pursuer.Velocity.get_length() )

        # now flee away from predicted future position of the pursuer
        return self.Flee(pursuer.Pos + pursuer.Velocity * lookAheadTime);

    def Wander( self ):
        """Man wanders randomly in the world"""
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

    def Pursuit( self, evader ):
        """Pursuit a target"""
        if not isinstance( evader, Game.Man.Man ):
            return

        # if the evader is ahead and facing the agent then we can just seek
        # for the evader's current position.
        toEvader = evader.Pos - self.Owener.Pos
        relativeHeading = self.Owener.Heading.dot( evader.Heading )
        
        if toEvader.dot( self.Owener.Heading ) > 0 and relativeHeading < -0.95: # acos( -0.95 ) = 18 degrees
            return self.Seek( evader.Pos )

        # Not ahead
        # the lookahead time is propotional to the distance between the evader
        # and the pursuer; and is inversely proportional to the sum of the
        # agent's velocities
        lookAheadTime = toEvader.get_length() / ( self.Owener.MaxSpeed + evader.Velocity.get_length() )

        # now seek to the predicted future position of the evader
        return self.Seek(evader.Pos + evader.Velocity * lookAheadTime);

    def Arrive( self, targetPos, arriveMode ):
        """ it attempts to arrive at the target with a zero velocity"""
        if not isinstance( targetPos, Vector2D ) or not isinstance( arriveMode, ArriveMode ):
            return

        toTarget = targetPos - self.Owener.Pos
        dist = toTarget.get_length()

        if dist > 0:
            arriveModeTweaker = 0.3
            speed = dist / ( float(self.ArriveMode) * arriveModeTweaker )
            speed = min( [ speed, self.Owener.MaxSpeed ] )
            desiredVelocity = toTarget * speed / dist
            return ( desiredVelocity - self.Owener.Velocity )

        return Vector2D( 0, 0 )
        pass

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

#########################################
###              Switchs
#########################################

    def On( self, behavior ):
        return self.iFlags&behavior == behavior

    def WanderOn( self ):
        self.iFlags = self.iFlags | BehaviorType.WANDER
    def WanderOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.WANDER

    def SeekOn( self ):
        self.iFlags = self.iFlags | BehaviorType.SEEK
    def SeekOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.SEEK

    def FleeOn( self ):
        self.iFlags = self.iFlags | BehaviorType.FLEE
    def FleeOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.FLEE

    def EvadeOn( self, target ):
        self.iFlags = self.iFlags | BehaviorType.EVADE
        if isinstance( target, GameObject ):
            self.TargetAgent1 = target
    def EvadeOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.EVADE

    def CohesionOn( self ):
        self.iFlags = self.iFlags | BehaviorType.COHESION
    def CohesionOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.COHESION

    def PursuitOn( self, target ):
        self.iFlags = self.iFlags | BehaviorType.PURSUIT
        if isinstance( target, GameObject ):
            self.TargetAgent1 = target
    def PursuitOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.PURSUIT

    def ArriveOn( self ):
        self.iFlags = self.iFlags | BehaviorType.ARRIVE
    def ArriveOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.ARRIVE

    def AlignmentOn( self ):
        self.iFlags = self.iFlags | BehaviorType.ALLIGNMENT
    def AlignmentOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.ALLIGNMENT
