import pygame, sys
from pygame.locals import *
from GUI.Colors import Colors
from GUI.DisplayScreen import DisplayScreen

pygame.init()

# set up the window
DISPLAYSURF = DisplayScreen.DisplaySurface
pygame.display.set_caption('Drawing')
# set up the colors

# draw on the surface object
DISPLAYSURF.fill(Colors.White)

# run the game loop
while True:
    for event in pygame.event.get():
         if event.type == QUIT:
             pygame.quit()
             sys.exit()

    

    pygame.display.update()