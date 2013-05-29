import pygame, sys
from pygame.locals import *
from Queue import Queue
import threading
import time
import datetime


##########################################
### Thread Manager class
##########################################

updateCellCount = 0
BeginUpdateEvent = threading.Event()
#UpdateFinishedEvent = threading.Event()

class CellThread(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, cellSpace ):
        threading.Thread.__init__(self)  
        self.thread_stop = False
        self.__timeElapsed__ = 0
        self.cellSpace = cellSpace
        #self.BeginUpdateEvent = threading.Event()

    def __del__( self ):
        self.Stop()
        threading._shutdown()

    def run(self): #Overwrite run() method, put what you want the thread do here  
        while not self.thread_stop:
            BeginUpdateEvent.wait()
            global updateCellCount
            
            if( updateCellCount < ThreadManager.totalThreadCount ):
                # Update each member in the cell
                #print str(len(self.cellSpace.Members)) + " members"
                for man in self.cellSpace.Members:
                    man.Update( self.__timeElapsed__ )

                #ThreadManager.postUpdateQueue.put_nowait( (self.thread_name, "_VALUE") )
                updateCellCount = updateCellCount + 1
            if updateCellCount >= ThreadManager.totalThreadCount:
                #UpdateFinishedEvent.set() 
                BeginUpdateEvent.clear()
                pass
            
            self.__timeElapsed__ = 0

    def Stop(self):
        self.thread_stop = True

    def Update( self, timeElapsed ):
        self.__timeElapsed__ = self.__timeElapsed__ + timeElapsed;
        #self.BeginUpdateEvent.set()
        

class ThreadManager:

    # TODO: Change this
    totalThreadCount = 1
    postUpdateQueue = Queue()
    threadPool = list()

    def __init__( self, CellSpace ):
        self.CellsSpace = CellSpace
        self.totalThreadCount = CellSpace.GameWorld.CellsX * CellSpace.GameWorld.CellsY
        if isinstance(self.CellsSpace.Cells, list):
            for cell in self.CellsSpace.Cells:
                newThread = CellThread( cell )
                self.threadPool.append( newThread )

        # 1. start all the update threads 
        for cellthread in self.threadPool:
            cellthread.start()

    def __del__(self):
        pass

    def Update( self, timeElapsed ):
        global updateCellCount
        updateCellCount = 0

        # 1. update threads will give some job to this thread
        for cellthread in self.threadPool:
            cellthread.Update( timeElapsed )
            #print len(cellthread.cellSpace.Members)
        BeginUpdateEvent.set()

        #print "wait"
        # 2. wait for all the update threads finish their jobs
        #UpdateFinishedEvent.wait()
        #print "post process"
        # 3. post process the postUpdateDict
        while True:
            try:
                tuple = ThreadManager.postUpdateQueue.get_nowait()
                self.CellsSpace.UpdateEntity_NoBlock( tuple[0], tuple[1] )
            except:
                break
        ThreadManager.postUpdateQueue = Queue()
        #UpdateFinishedEvent.clear()
