import pygame, sys
from pygame.locals import *
from Queue import Queue
import threading
import time

##########################################
### Thread Manager class
##########################################

updateCellCount = 0
#BeginUpdateEvent = threading.Event()
UpdateFinishedEvent = threading.Event()

class CellThread(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, name):
        threading.Thread.__init__(self)  
        self.thread_name = name  
        self.thread_stop = False
        self.__timeElapsed__ = 0
        self.BeginUpdateEvent = threading.Event()

    def __del__( self ):
        self.Stop()
        threading._shutdown()

    def run(self): #Overwrite run() method, put what you want the thread do here  
        while not self.thread_stop:
            self.BeginUpdateEvent.wait()
            global updateCellCount
            
            if( updateCellCount < ThreadManager.totalThreadCount ):
                print self.thread_name;
                ThreadManager.postUpdateQueue.put_nowait( (self.thread_name, "_VALUE") )
                updateCellCount = updateCellCount + 1
            if updateCellCount >= ThreadManager.totalThreadCount:
                UpdateFinishedEvent.set() 
                pass
            self.BeginUpdateEvent.clear()

    def Stop(self):
        self.thread_stop = True

    def Update( self, timeElapsed ):
        self.__timeElapsed__ = timeElapsed;
        self.BeginUpdateEvent.set()


class ThreadManager:

    totalThreadCount = 4
    postUpdateQueue = Queue()

    def __init__( self ):
        self.thread1 = CellThread( "Thread_1_" )
        self.thread2 = CellThread( "Thread_2_" )
        self.thread3 = CellThread( "Thread_3_" )
        self.thread4 = CellThread( "Thread_4_" )

        # 1. start all the update threads 
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        self.thread4.start()

    def __del__(self):
        pass

    def Update( self, timeElapsed ):
        global updateCellCount
        updateCellCount = 0

        print timeElapsed

        # 1. update threads will give some job to this thread
        self.thread1.Update( timeElapsed )
        self.thread2.Update( timeElapsed )
        self.thread3.Update( timeElapsed )
        self.thread4.Update( timeElapsed )

        # 2. wait for all the update threads finish their jobs
        UpdateFinishedEvent.wait()
        # 3. post process the postUpdateDict
        time.sleep( 1 )
        while True:
            try:
                print ThreadManager.postUpdateQueue.get_nowait()
            except:
                break
        ThreadManager.postUpdateQueue = Queue()
        time.sleep( 2 )


##########################################
### Test Game World class
##########################################
class TestGameWorld:
    def __init__(self):
        print "Begin Test Game World"
        self.CellThreadManager = ThreadManager()

        pass

    def Update(self, timeElapsed):
        #print timeElapsed;
        self.CellThreadManager.Update( timeElapsed )



##########################################
### Main Thread
##########################################
pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')

# Setupt Game World
gameWorld = TestGameWorld()

# Setup Timer
fpsTimer = pygame.time.Clock()
fpsTimer.tick()


while True: # main game loop
     for event in pygame.event.get():
         if event.type == QUIT:
             pygame.quit()
             sys.exit()
     timeInSecond = fpsTimer.tick() / 1000.0 # Get the elapsed time in second


     gameWorld.Update( timeInSecond )
     pygame.display.update()

