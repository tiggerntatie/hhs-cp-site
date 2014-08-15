import pygame
from pygame.locals import *

WIDTH = 600
HEIGHT = 300
WINDOW_DIMENSIONS = (WIDTH, HEIGHT)
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
# some variables to define an oscillating circle
RADIUS = 50                                                 # circle radius, pixels
LINEWIDTH = 1                                               # circle line width, pixels

XMIN = RADIUS                                               # minimum x position
XMAX = WIDTH - RADIUS                                       # maximum x position
YMIN = RADIUS
YMAX = HEIGHT - RADIUS
FPS = 100                                                   # how many frames per second do we want?

position = [XMIN, YMIN]                                     # define a starting x,y
velocity = [240, 60]                                        # pick some numbers, pixels/second

# start setting up Pygame
pygame.init()
displaysurface = pygame.display.set_mode(WINDOW_DIMENSIONS)
pygame.display.set_caption('Pygame Animate 1')
clock = pygame.time.Clock()                                 # make a clock object to manage a frame rate

done = False
while not done:                                             # main game loop
    elapsedms = clock.tick(FPS)                             # forces WAIT to maintain FPS

    # compute a new position for the circle based on old position and velocity 
    position = [p + v/FPS for p,v in zip(position, velocity)] 
                                                            # v/FPS computes pixels/frame instead of pixels/second
                                                            # resulting position is a tuple of floats!
    
    # check to see if the circle is outside the margin
    if ((position[0] > XMAX and velocity[0] > 0) or          
        (position[0] < XMIN and velocity[0] < 0)):          # outside left/right margin?
        velocity[0] *= -1                                   # reverse the x velocity

    if ((position[1] > YMAX and velocity[1] > 0) or          
        (position[1] < YMIN and velocity[1] < 0)):          # outside top/bottom margin?
        velocity[1] *= -1                                   # reverse the x velocity

    displaysurface.fill(BLACK)                              # erase the entire display surface
    pygame.draw.circle(displaysurface, 
                        WHITE, 
                        [int(x) for x in position],         # position must be passed with integer parts
                        RADIUS, 
                        LINEWIDTH)                          # draw a circle directly to the display surface
    
    pygame.display.update()                                 # refresh the display screen (display what we have done)
    
    for event in pygame.event.get():                        # check for events
        if event.type == QUIT:
            done = True
        else:
            print(event)                                    # see the variety of events that pygame knows about