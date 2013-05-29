import pygame, sys
from pygame.locals import *
from GUI.Colors import Colors
from GUI.DisplayScreen import DisplayScreen
from Game.GameWorld import GameWorld
from GUI.GUIFonts import GUIFonts

pygame.init()

# set up the window
DISPLAYSURF = DisplayScreen.DisplaySurface
pygame.display.set_caption('Drawing')
# set up the colors

# draw on the surface object
backgroundColor = Colors.White
DISPLAYSURF.fill(backgroundColor)
DISPLAYSURF.blit
Font = GUIFonts()
fpsText = Font.create_text("FPS: ", DisplayScreen.Font_preferences, 20, (0, 128, 0))

# Setup the game world
gameWorld = GameWorld()

# Setup Timer
fpsTimer = pygame.time.Clock()
fpsTimer.tick()


# run the game loop
while True:
    for event in pygame.event.get():
         if event.type == QUIT:
             pygame.quit()
             sys.exit()


    timeInSecond = fpsTimer.tick() / 1000.0 # Get the elapsed time in second
    fpsText = Font.create_text("FPS: " + str( fpsTimer.get_fps() ), DisplayScreen.Font_preferences, 20, (0, 128, 0))

    gameWorld.Update( timeInSecond )
    DISPLAYSURF.fill( backgroundColor )
    DISPLAYSURF.blit(fpsText, ( 0, 0 ))

    gameWorld.Render()
    pygame.display.flip()
    if( gameWorld.MultiThreadUpdate ):
        pygame.time.wait( 30 )
    