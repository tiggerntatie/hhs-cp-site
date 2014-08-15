import pygame
from pygame.locals import *

# make some convenient color objects
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')

# Display some simple shapes with semi-transparency

pygame.init()
pygame.display.set_caption('Hello World!')
displaysurface = pygame.display.set_mode((400,400))
drawsurface = displaysurface.copy()                                 # get a screen copy to draw on
drawsurface.set_colorkey(BLACK)                                     # the color black will be TRANSPARENT

done = False
while not done:                                                     # main game loop
    # ALWAYS ERASE THE DISPLAY SURFACE
    displaysurface.fill(BLACK)
    # BEGIN DRAWING A RECTANGLE
    drawsurface.fill(BLACK)                                         # clear the drawing surface to TRANSPARENT
    pygame.draw.rect(drawsurface, WHITE, pygame.Rect(20,20,200,300)) # draw a rectangle on the drawing surface    
    drawsurface.set_alpha(100)                                       # make the surface semi-transparent
    displaysurface.blit(drawsurface,(0,0))                          # copy ('blit') the drawing surface to the display
    # BEGIN DRAWING A RED CIRCLE
    drawsurface.fill(BLACK)                                         # clear the drawing surface again (fill black)
    pygame.draw.circle(drawsurface, RED, (200,200),86)              # draw a circle on the drawing surface
    drawsurface.set_alpha(150)                                      # relatively opaque
    displaysurface.blit(drawsurface,(0,0))                          # copy ('blit') to the display surface again
    # BEGIN DRAWING A BLUE CIRCLE ON A SMALL SURFACE
    smallsurf = pygame.Surface((200,200))                           # create a smaller drawing surface
    smallsurf.set_colorkey(BLACK)                                   # say that black will be TRANSPARENT here too
    pygame.draw.circle(smallsurf, BLUE, (86,86),86)                 # and draw a circle to it
    smallsurf.set_alpha(220)                                        # almost completely opaque
    displaysurface.blit(smallsurf,(200,200))                        # then copy it to the display surface
    # REFRESH THE SCREEN
    pygame.display.update()                                         # make the display surface appear on the computer screen
    pygame.time.wait(10)                                            # wait for 10 milliseconds
                                    
    for event in pygame.event.get():                                # check for events
        if event.type == QUIT:                                      # stop the main game loop if QUIT is received
            done = True
        else:
            print(event)                                            # see unhandled events going by