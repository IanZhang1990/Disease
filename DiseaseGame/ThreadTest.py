import pygame, sys
from pygame.locals import *
import threading
import time

##########################################
### Thread Manager class
##########################################
class ThreadTimer(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, num, interval):  
        threading.Thread.__init__(self)  
        self.thread_num = num  
        self.interval = interval  
        self.thread_stop = False  
   
    def run(self): #Overwrite run() method, put what you want the thread do here  
        while not self.thread_stop:  
            print 'Thread Object(%d), Time:%s\n' %(self.thread_num, time.ctime())  
            time.sleep(self.interval)  

    def stop(self):  
        self.thread_stop = True

##########################################
### Test Game World class
##########################################
class TestGameWorld:
    def __init__(self):
        print "Begin Test Game World"
        pass

    def Update(self, timeElapsed):
        print timeElspsed;



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

