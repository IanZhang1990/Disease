#=====================================================================================
# Filename: Man.py
# Author: Ian Zhang
# Description: This file defines Man class, 
#               which defines properties and methods of a man.
#=====================================================================================
import Game.Virus
import time


class Man(object):
    """Man class defines properties and methods of a man"""

    def __init__(self):
        self.Sex = str("Male")                            # By default, the man is a male.
        self.Disease = Null                                 # Virus
        self.Age = 20                                         # Age
        self.Sickness = 0.0                                 # Not yet sick
        self.City = Null                                      # In Null City
        self.Steering = Null                               # SteeringBehavior
        self.LeftIncubationDay = 0                    # Not infected man have no incubation day
        self.DateGetInfected = Null;                        # The date the man got sick
        self.SickTime = 0                                   # Duration of being sick
        self.MetList = []                                    # The list of man he met after getting infected.
        self.Quarantine = False                          # Not infected, not quarantined.
        self.ManStateMachine = Null                 # A man's statemachine

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
        return (self.Disease != Null)
        
