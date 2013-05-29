import pygame, sys
from pygame.locals import *
from Queue import Queue
import threading
import time
import datetime

##########################################
### Thread Manager class
##########################################

updatedCells = list()
BeginUpdateEvent = threading.Event()
UpdateFinishedEvent = threading.Event()
#global_TimeElapsed = 0.0

class CellThread(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, cellSpace ):
        threading.Thread.__init__(self)  
        self.thread_stop = False
        self.__timeElapsed__ = 0
        self.cellSpace = cellSpace
        self.LastUpdateTimeStamp = time.clock()

    def __del__( self ):
        self.Stop()
        threading._shutdown()

    def run(self): #Overwrite run() method, put what you want the thread do here  
        while not self.thread_stop:
            global updatedCells
            #BeginUpdateEvent.wait()
            #time.sleep( 0.02 )

            try:
            #    idx = updatedCells.index( self )
            #except ValueError:
                # Update each member in the cell
                currentTime = time.clock()
                self.__timeElapsed__ = (currentTime - self.LastUpdateTimeStamp)
                self.LastUpdateTimeStamp = currentTime
                #print self.__timeElapsed__
                for man in self.cellSpace.Members:
                    #self.__timeElapsed__ = global_TimeElapsed
                    man.Update( self.__timeElapsed__ )
                #ThreadManager.postUpdateQueue.put_nowait( (self.thread_name, "_VALUE") )
                #updatedCells.append( self )
                self.__timeElapsed__ = 0
                pass
            finally:
                #if len( updatedCells )  >= ThreadManager.totalThreadCount :
                #    UpdateFinishedEvent.set()
                #    BeginUpdateEvent.clear()
                pass

    def Stop(self):
        self.thread_stop = True

    def Update( self, timeElapsed ):
        self.__timeElapsed__ = self.__timeElapsed__ + timeElapsed;
        

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
        for cellthread in self.threadPool:
            cellthread.Stop()   
        pass

    def Update( self, timeElapsed ):
        global updatedCells
        global BeginUpdateFlag
        global global_TimeElapsed
            

        # 1. update threads will give some job to this thread
        #BeginUpdateEvent.set()
        #for cellthread in self.threadPool:
        #    cellthread.Update( timeElapsed )        

 
        # 2. wait for all the update threads finish their jobs
        #UpdateFinishedEvent.wait()
        #while len(updatedCells) < self.totalThreadCount:
        #    time.sleep( 0.030 )

        #continue
        #BeginUpdateEvent.clear()
        #updatedCells = list()

        #print "process"
        # 3. post process the postUpdateDict
        while True:
            try:
                tuple = ThreadManager.postUpdateQueue.get_nowait()
                self.CellsSpace.UpdateEntity_NoBlock( tuple[0], tuple[1] )
            except:
                break
        #ThreadManager.postUpdateQueue = Queue()
        #UpdateFinishedEvent.clear()
