import pygame, sys
from pygame.locals import *
from GUI.Colors import Colors, Colors, Colors
from GUI.DisplayScreen import DisplayScreen
from Game.GameWorld import GameWorld

pygame.init()

# set up the window
DISPLAYSURF = DisplayScreen.DisplaySurface
pygame.display.set_caption('Drawing')
# set up the colors

# draw on the surface object
DISPLAYSURF.fill(Colors.White)

# Setup Timer
fpsTimer = pygame.time.Clock()
fpsTimer.tick()

posX = 0;

# run the game loop
while True:
    for event in pygame.event.get():
         if event.type == QUIT:
             pygame.quit()
             sys.exit()

    timeInSecond = fpsTimer.tick() / 1000 # Get the elapsed time in second
    
    pygame.draw.circle( DisplayScreen.DisplaySurface, Colors.Green, ( int(posX), 200 ), 5 )    

    posX += 0.2
    posX %= 600

    pygame.display.update()