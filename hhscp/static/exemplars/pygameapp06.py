import pygame
from pygame.locals import *

class PygameApp(object):
    """
    Class that encapsulates a basic pygame application.
    """
    def __init__(self, screensize = (400,400), fullscreen = False, title = 'PygameApp Window'):
        """
        Argument to initializer is the desired screen size and/or desire for full screen
        """
        # save copies of the creation arguments
        self.screensize = screensize
        self.fullscreen = fullscreen
        self.title = title

        # create a pygame group for tracking sprites
        self.spritegroup = pygame.sprite.LayeredDirty() 
        
        self.elapsedms = 0                          # keep track of the elapsed time
        
        pygame.init()                               # every pygame app must do this
        self.clock = pygame.time.Clock()            # make a clock object to manage a frame rate
        
        # open a window different ways, depending on fullscreen setting
        if self.fullscreen:
            # find out what the current display capabilities are
            self.displayinfo = pygame.display.Info()
            self.screensize = (self.displayinfo.current_w, self.displayinfo.current_h)
            self.display = pygame.display.set_mode(self.screensize, FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(self.screensize) # create a window
            pygame.display.set_caption(self.title)
        self.setbackgroundcolor(pygame.Color('black'))

    def setbackgroundcolor(self, color):
        self.backgroundcolor = color
        self.erase()

    def erase(self):
        self.display.fill(self.backgroundcolor)
        self.background = self.display.copy()       # Create a cleared background surface

    def run(self, fps = 50):
        """
        Begin display loop. Optional argument sets the frames per second desired.
        """
        self.fps = fps
        running = True
        # repeat the display loop
        while running:
            # get events
            for event in pygame.event.get():
                if event.type != QUIT:
                    running = self.handle_event(event)  # let the user event handler deal with it
                else:
                    running = False
            self.elapsedms += self.clock.tick(self.fps)
            # do any regular, periodic processing
            self.poll()
            self.spritegroup.clear(self.display, self.background)       # erase sprite backgrounds as needed
            pygame.display.update(self.spritegroup.draw(self.display))  # update the display
        # fell out of loop
        self.quit()

    def quit(self):
        """
        Close up and quit. Override this method as desired.
        """
        pygame.quit()


    def handle_event(self, event):
        """
        Deal with any events OTHER than QUIT, which is handled elsewhere. This method SHOULD
        be overridden in your own application.
        """
        return True                                     # default: keep running

    def poll(self):
        """
        Do any processing that should be done on each frame. This method SHOULD
        be overridden in your own application.
        """
        pass




# Circle class extends DirtySprite

class Circle(pygame.sprite.DirtySprite):
    """
    Custom version of DirtySprite that draws a circle - initializer must accept a group or list of groups
    """
    def __init__(self, *groups):
        super().__init__(groups)                # Call the base class initializer with the groups
        self.suppressupdate = True              # delay updating image until finished 
        self.color = pygame.Color('white')      # default color is black, opaque
        self.thickness = 2                      # default thickness is two pixels
        self.setpos((100,100))                  # set a default location for the circle
        self.setradius(50)                      # set a default radius
        self.setfilled(False)                   # default drawing style
        self.suppressupdate = False
        self.updateimage()                      # Create the image and rect members

    def updateimage(self):
        """
        Redraw the circle image using correct color and thickness
        """
        if not self.suppressupdate:
            circlebackground = pygame.Color('black')
            self.image = pygame.Surface((self.radius*2, self.radius*2)) 
            self.image.fill(circlebackground)           # fill the background with transparent BLACK
            self.image.set_colorkey(circlebackground)   # BLACK will be transparent
            self.rect = self.image.get_rect()           # generate the sprite rect member (REQUIRED)
            self.rect.center = self.pos                 # reposition it 
            if self.filled:                             # draw the circle image on the surface
                pygame.draw.circle(self.image, self.color,(self.radius, self.radius),self.radius)
            else:
                pygame.draw.circle(self.image, self.color,(self.radius, self.radius),self.radius, self.thickness)
            self.dirty = 1                              # force redraw

    def setradius(self, radius):
        """
        Set the radius of the circle and redraw. This rarely changes.
        """
        if radius >= self.thickness:
            self.radius = radius
            self.updateimage()

    def setpos(self, pos):
        """
        Set the location of the circle center (pass in a x,y tuple)
        """
        self.pos = pos
        self.updateimage()

    def setcolor(self, color):
        """
        Set a new color for the circle (pass in a (r,g,b,alpha) tuple)
        """
        self.color = color
        self.updateimage()

    def setthickness(self, thickness):
        """
        Set a new line thickness in pixels
        """
        if thickness <= self.radius:
            self.thickness = thickness
            self.updateimage()

    def setfilled(self, filled):
        """
        Set flag indicating filled circle (or not)
        """
        self.filled = filled
        self.updateimage()


    def copy(self):
        """
        Make a copy of the circle and return it
        """
        circ = Circle(self.groups())    # make a new circle, using the same groups that this one has
        circ.setpos(self.pos)           # give it the same parameters as this one
        circ.setradius(self.radius)
        circ.setcolor(self.color)
        circ.setthickness(self.thickness)
        circ.setfilled(self.filled)
        return circ
