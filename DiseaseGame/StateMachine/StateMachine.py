#=====================================================================================
# Filename: StateMachine.py
# Author: Ian Zhang
# Description: This file defines StateMachine related classes, 
#  
#=====================================================================================


#===========================================================
#           State Class
#===========================================================
class State:
    """Summary: 
        Abstract base class to define an interface for a state
    """
    def Enter( self, gameObject ):
        """Execute when the state is entered"""
        pass;
    def Execute( self, gameObject ):
        """This state's normal update function"""
        pass;
    def Exit( self, gameObject ):
        """Execute when the state is exited"""
        pass;
    def OnMessage( self, gameObject, telegram ):
        """Execute when the agent receives a message from the message dispatcher"""
        pass;


#===========================================================
#           StateMachine Class
#===========================================================
class StateMachine:
    """abstract base class to define statemachine behavior"""
    def __init__( self, gameObj ):
        """Constructor for StateMachine Class"""
        self.Owener = gameObj                                         # A pointer to the agent that owns this instance
        self.CurrentState = None;                                      # A record of the current state the agent is in
        self.PreviousState = None;                                      # A record of the last state the agent was in
        self.GlobalState = None;                                        # this is called every time the FSM is updated
   
    def SetCurrentState( self, state ):
        """To set the current state of the agent"""
        self.CurrentState = state

    def SetGlobalState( self, globalState ):
        self.GlobalState = globalState

    def SetPreviousState( self, prvState ):
        self.PreviousState = prvState

    def IsInState( self, state ):
        if type(self.CurrentState) == type( state ):
            return true
        else:
            return false

    def Update(self):
        """Update the FSM"""
        # if a global state exist, execute
        if( self.GlobalState != None ):
            self.Globalstate.Execute( self.Owener )

        # same for the current state
        if( self.CurrentState != None ):
            self.CurrentState.Execute( self.Owener )

    def HandleMessage( self, message ):
        """This method has not been implemented, yet!!!"""
        print 'StateMachine::HandleMessage method has not been implemented, yet!!!'

    def ChangeState( self, newState ):
        """change to a new state"""
        if newState != None:
            # Keep a record of the previous state
            self.PreviousState = self.CurrentState;

            # Call the Exit method of current state to exit
            self.CurrentState.Exit( self.Owener )

            # Change State to the new state
            self.CurrentState = newState;

            # Call the Enter method of the new state
            self.CurrentState.Enter( self.Owener )

    def RevertToPrevState( self ):
        """Change state back to the previous state"""
        self.ChangeState( self.PreviousState )