#=====================================================================================
# Filename: Man.py
# Author: Ian Zhang
# Description: This file defines Man class, 
#               which defines properties and methods of a man.
#=====================================================================================
import Game.Virus
import time
from Utils.SteeringBehavior import SteeringBehavior
from Math.Vector import Vector2D
from Math.Math2D import Math2D
import pygame
from GUI.DisplayScreen import DisplayScreen
from GUI.Colors import Colors
from Utils.FileOperation import ParameterLoader

#===========================================================
#           ManParamLoader Class
#===========================================================
class ManParamLoader(ParameterLoader):
    """Summary:
        This parameter loader is designed for loading virus parameters only.

        A .man file contains parameters:
        AgentNumber
        Mass
        Size
        MaxForce
        MaxSpeed
        Scale
        ViewDistance
    """

    def __init__( self, manFilename ):
        """Summary:
            Constructor of manParamLoader Class
            Parameters:
            manFilename:  The name of the file that defines parameters of men. It has to be ended with ".man"
        """
        if( str(manFilename).endswith('.man') ):
            ParameterLoader.__init__(self, manFilename);
            ParameterLoader.LoadFile(self);

class Man(object):
    """Man class defines properties and methods of a man"""

    def __init__(self, world, manParmLoader, steeringParmLoader, sex, age, position, velocity):
        self.Sex = str("Male")                            # By default, the man is a male.
        self.Disease = None                                 # Virus
        self.Age = 20                                         # Age
        self.Sickness = 0.0                                 # Not yet sick
        self.City = None                                      # In None City
        self.World = world                                # The game world the man is in
        self.Steering = None                               # SteeringBehavior
        self.LeftIncubationDay = 0                    # Not infected man have no incubation day
        self.DateGetInfected = None;                  # The date the man got sick
        self.SickTime = 0                                   # Duration of being sick
        self.MetList = []                                    # The list of man he met after getting infected.
        self.Quarantine = False                          # Not infected, not quarantined.
        self.ManStateMachine = None                 # A man's statemachine
        self.DrawingColor = Colors.Green           # A normal man looks green.

        # Get Parameters from Parameter Loader
        self.MaxSpeed = float(manParmLoader.Parameters.get('MaxSpeed', 20));
        self.MaxForce = float(manParmLoader.Parameters.get('MaxForce'));
        self.Mass = float(manParmLoader.Parameters.get('Mass'));
        self.Size = float(manParmLoader.Parameters.get('Size'));
        self.Scale = float(manParmLoader.Parameters.get('Scale'));
        self.ViewDistance = float(manParmLoader.Parameters.get('ViewDistance'));

        # Create Steering Behavior
        self.Steering = SteeringBehavior( self, steeringParmLoader)
        self.Sex = sex
        self.Age = age
        self.Pos = position
        self.Velocity = velocity


    def GetInfect( self, virus ):
        """Get Infect from the infector"""
        self.Disease = virus;
        self.Sickness = 0.01                                # Once get infected, you are 1% sick
        self.DateGetInfected = time.localtime();  # Record the date get infected

    def MeetSomeone( self, man ):
        """Call the function when meet someone"""
        # Test if the meeting man is a virus carrier.
        # Test the possibility of getting the virus if the meeting man is a virus carrier.
        
    def GetInfectedPosibility( self, virus ):
        """Is threatened of getting such virus? Call the Method when meet a sick person to see
            the posibility of getting a certain virus"""
        # Test Age and Sex to see if possible to get sick
        # Get the virus' infection rate. And test determine if the man will get sick. 
        # If get sick, call GetInfect()
    
    def IsInfected(self):
        """True, if the man is infected by a virus"""
        return (self.Disease != None)
        



    ##########################################################
    def Render( self ):
        """Render the man into the screen"""
        pygame.draw.circle( DisplayScreen.DisplaySurface, self.DrawingColor, self.Pos, self.Size )        

    def Update(self, elapsedTime):
        """Update the man's state"""
        self.ElaplsedTime = elapsedTime;      # Update the elapsedTime
        oldPos = self.Pos                              # Keep a record of 

        steeringForce = Vector2D( 0, 0)
        steeringForce = self.Steering.Calculate();
        if steeringForce is None:
            pass

        acceleration = steeringForce / self.Mass
        self.Velocity += acceleration * elapsedTime
        self.Velocity.Truncate( self.MaxSpeed )          # make sure the velocity does not exceed maximum speed
        self.Pos = self.Pos + self.Velocity * elapsedTime # Update position information

        # Update the heading if the vehicle has a non zero velocity
        if self.Velocity.get_length_sqrd() > 0.00000001:
            self.Heading = self.Velocity.normalized()
            self.Side = self.Heading.perpendicular()

        # Treat the screen as a toroid
        Math2D.WrapAround( self.Pos, self.World.WorldWidth, self.World.WorldHeight )

        # Update the vehicle's current cell if space partitioning is turned on
        if self.Steering.IsPacePartitionOn():
            print 'Not Implemented Yet'