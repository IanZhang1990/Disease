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
import Math


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
        if not isinstance( parmLoader, SteeringParmLoader ):
            return
        self.Owener = owener
        self.Path = None
        self.SteeringForce = Vector2D(0, 0)

        self.iFlags = 0             # binary flags to indicate whether or not a behavior should be active
        # These can be used to keep track of friends, pursuers, or prey
        self.TargetAgent1 = None
        self.TargetAgent2 = None
        self.Target = None       # The current target

        self.DBoxLength = float(parmLoader.Parameters.get('MinDetectionBoxLength', 40.0))        # length of the 'detection box' utilized in obstacle avoidance
        self.DBoxLength_RawValue = self.DBoxLength
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

    def ObstacleAvoidance(self, obstacleList):
        """this returns a steering force which will attempt to keep the agent 
            away from any obstacles it may encounter"""
        if not isinstance( obstacleList, list ):
            return 
        #the detection box length is proportional to the agent's velocity
        self.DBoxLength = self.DBoxLength_RawValue + self.Owener.Velocity.get_length() / self.Owener.MaxSpeed() *self.DBoxLength_RawValue
        #tag all obstacles within range of the box for processing
        self.Owener.World.TagObstaclesWithinViewRange( self.Owener, self.DBoxLength )
        
        ClosestIntersectingObstacle = None                  # keep track of the closest intersecting obstacle (CIB)
        DistToClosestIP = 10000000000000.0             # track the distance to the CIB
        LocalPosOfClosestObstacle = Vector2D( 0, 0 )   # the transformed local coordinates of the CIB

        for obstacle in obstacleList:
            if obstacle.IsTagged():
                localPos = Math.Math2D.Transformations.PointToLocalSpace( obstacle.Pos, self.Owener.Heading, self.Owener.Side, self.Owener.Pos )
                # if the local position has a negative x value then it must lay
                # behind the agent. (in which case it can be ignored)
                if localPos.x > 0:
                    # if the distance from the x axis to the object's position is less
                    # than its radius + half the width of the detection box then there
                    # is a potential intersection.
                    expandedRadius = obstacle.BoundingRadius + self.Owener.BoundingRadius
                    if math.fabs( localPos.y ) < expandedRadius:
                        # now to do a line/circle intersection test. The center of the 
                        # circle is represented by (cX, cY). The intersection points are 
                        # given by the formula x = cX +/-sqrt(r^2-cY^2) for y=0. 
                        # We only need to look at the smallest positive value of x because
                        # that will be the closest point of intersection.
                        cx = localPos.x
                        cy = localPos.y
                        # we only need to calculate the sqrt part of the above equation once
                        sqrtPart = math.sqrt( expandedRadius * expandedRadius - cy * cy )
                        ip = cx - sqrtPart
                        if ip <= 0.0:
                            ip = cx + sqrtPart
                            pass
                        # test to see if this is the closest so far. If it is keep a
                        # record of the obstacle and its local coordinates
                        if ip < DistToClosestIP:
                            DistToClosestIP = ip
                            ClosestIntersectingObstacle = obstacle
                            LocalPosOfClosestObstacle = localPos
                            pass
                        pass
                    pass
                pass
            pass

        # if we have found an intersecting obstacle, calculate a steering force away from it
        steeringForce = Vector2D( 0, 0 )

        if ClosestIntersectingObstacle is not None:
            # the closer the agent is to an object, the stronger the steering force should be
            multiplier = 1.0 + (self.DBoxLength - LocalPosOfClosestObstacle.x) / self.DBoxLength;
            steeringForce.y = ( ClosestIntersectingObstacle.BoundingRadius - LocalPosOfClosestObstacle.y ) * multiplier ################################## Something you can add here 
            brakingWeight = 0.2
            steeringForce.x = ( ClosestIntersectingObstacle.BoundingRadius - LocalPosOfClosestObstacle.x ) * brakingWeight ################################## Something you can add here 
            pass

        return Math.Math2D.Transformations.VectorToWorldSpace( steeringForce, self.Owener.Heading, self.Owener.Side )
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

    def FollowPath( self ):
        if( self.Path.CurrWayPoint - self.Owener.Pos ).get_length_sqrd() < self.WaypointSeekDistSq:
            self.Path.SetNextWaypoint()
        if self.Path.Finished:
            return self.Seek( self.Path.CurrWayPoint )
        else:
            return self.Arrive( self.Path.CurrWayPoint, ArriveMode.NORMAL )

#----------------- Group Behaviors ----------------
    def Cohesion( self, neighbors ):
        """returns a steering force that attempts to move the agent towards the
            center of mass of the agents in its immediate area.
            USES SPACIAL PARTITIONING"""
        if not isinstance( neighbors, list ):
            return
        # first find the center of mass of all the agents
        centerOfMass = Vector2D( 0, 0 )
        steeringForce = Vector2D( 0, 0 )

        # iterate through the neighbors and sum up all the position vectors
        neighborCount = 0
        entity = self.Owener.World.CellSpace.FirstNeighbor()
        while not self.Owener.World.CellSpace.EndNeighbor():
            if entity != self.Owener:
                centerOfMass = centerOfMass + entity.Pos
                neighborCount = neightborCount + 1
                pass
            entity = self.Owener.World.CellSpace.NextNeighbor()
            pass

        if neighborCount > 0:
            centerOfMass = centerOfMass / float( neighborCount )
            # now seek towards that position
            steeringForce = self.Seek( centerOfMass )
            pass

        # the magnitude of cohesion is usually much larger than separation or
        # allignment so it usually helps to normalize it.
        return steeringForce.normalized()

    def Alignment( self, neighbors ):
        """returns a force that attempts to align this agents heading with that
            of its neighbors
            USES SPACIAL PARTITIONING"""
        avgHeading = Vector2D( 0, 0 )
        neighborCount = 0
        entity = self.Owener.World.CellSpace.FirstNeighbor()
        while not self.Owener.World.CellSpace.EndNeighbor():
            if entity != self.Owener:
                avgHeading = avgHeading + entity.Heading
                neighborCount = neightborCount + 1
                pass
            entity = self.Owener.World.CellSpace.NextNeighbor()
            pass
        # if the neighborhood contained one or more vehicles, average their
        # heading vectors.
        if neighborCount > 0:
            avgHeading = avgHeading / float(neighborCount)
            avgHeading = avgHeading - self.Owener.Heading
            pass
        return avgHeading




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

    def ObstacleAvoidanceOn(self):
        self.iFlags = self.iFlags | BehaviorType.OBSTACLE_AVOID
    def ObstacleAvoidanceOff(self):
        self.iFlags = self.iFlags ^ BehaviorType.OBSTACLE_AVOID

    def FollowPathOn( self ):
        self.iFlags = self.iFlags | BehaviorType.FOLLOW_PATH
    def FollowPathOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.FOLLOW_PATH

    # -------------- Group Behavior --------------------
    def AlignmentOn( self ):
        self.iFlags = self.iFlags | BehaviorType.ALLIGNMENT
    def AlignmentOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.ALLIGNMENT

    def SeparationOn(self):
        self.iFlags = self.iFlags | BehaviorType.SEPARATION
    def SeparationOff(self):
        self.iFlags = self.iFlags ^ BehaviorType.SEPARATION

    def CohesionOn( self ):
        self.iFlags = self.iFlags | BehaviorType.COHESION
    def CohesionOff( self ):
        self.iFlags = self.iFlags ^ BehaviorType.COHESION
