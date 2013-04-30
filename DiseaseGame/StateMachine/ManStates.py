#=====================================================================================
# Filename: ManStates.py
# Author: Ian Zhang
# Description: This file defines Man's states
#  
#=====================================================================================

from StateMachine.StateMachine import State
from StateMachine import StateMachine
import Game

#===========================================================
#           ManStateMachine Class
#===========================================================
class ManStateMachine( StateMachine ):
    """StateMachine for man"""
    def __init__( self, man ):
        if type(man) == type( Game.Man.Man ):
            StateMachine.__init__(self, man )
        else:
            raise TypeError()


#===========================================================
#           State Class
#===========================================================
class ManStates(State):
    """description of class"""


