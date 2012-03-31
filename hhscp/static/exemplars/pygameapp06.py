"""
Pygameapp06.py Pygame application and Circle sprite implementation.

Copyright (c) 2012 by E Dennison
"""

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
        pygame.init()  # every pygame app must start herep
        self.clock = pygame.time.Clock() # make a clock object to manage a frame rate
        self.spritegroup = pygame.sprite.LayeredDirty() # sprite group that tracks dirty
        # open a window different ways, depending on fullscreen setting
        if self.fullscreen:
            # find out what the current display capabilities are
            self.displayinfo = pygame.display.Info()
            self.screensize = (self.displayinfo.current_w, self.displayinfo.current_h)
            self.display = pygame.display.set_mode(self.screensize, FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(self.screensize) # create a window
            pygame.display.set_caption(self.title)
        self.setbackground((0,0,0))

    def setbackground(self, color):
        self.display.fill(color)
        self.background = self.display.copy()

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
                    self.handle_event(event)                            # let the user event handler deal with it
                else:
                    running = False
            # do any regular, periodic processing
            self.elapsedms = self.clock.tick(self.fps)
            self.poll()                                                 # any period processing not handled by sprites and/or event handling
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
        pass

    def poll(self):
        pass


# Circle class extends DirtySprite

class Circle(pygame.sprite.DirtySprite):
    """
    Custom version of DirtySprite that draws a circle - initializer must accept a group or list of groups
    """
    def __init__(self, *groups):
        super(Circle, self).__init__(groups)  # Call the base class initializer with the groups
        self.color = (0,0,0,255)  # default color is black, opaque
        self.thickness = 2        # default thickness is two
        self.rect = Rect((0,0,0,0))
        self.setpos((100,100))
        self.setradius(50)
        self.setfilled(False)
        self.update()             # Create the image and rect members

    def update(self, *args):
        """
        Redraw the circle image using correct color and thickness
        """
        self.image = pygame.Surface((self.radius*2, self.radius*2)).convert_alpha()
        self.image.fill((0,0,0,0))  # fill the background with transparent BLACK
        self.rect = self.image.get_rect()  # generate a new rectangle
        self.rect.center = self.pos  # reposition it
        if self.filled:
            pygame.draw.circle(self.image, self.color,(self.radius, self.radius),self.radius)
        else:
            pygame.draw.circle(self.image, self.color,(self.radius, self.radius),self.radius, self.thickness)
        self.dirty = 1      # force redraw

    def setradius(self, radius):
        """
        Set the radius of the circle and redraw. This rarely changes.
        """
        if radius >= self.thickness:
            self.radius = radius

    def setpos(self, posxy):
        """
        Set the location of the circle center (pass in a x,y tuple)
        """
        self.pos = posxy

    def setcolor(self, color):
        """
        Set a new color for the circle (pass in a (r,g,b,alpha) tuple)
        """
        self.color = color

    def setthickness(self, thickness):
        """
        Set a new line thickness in pixels
        """
        if thickness <= self.radius:
            self.thickness = thickness

    def setfilled(self, filled):
        """
        Set flag indicating filled circle (or not)
        """
        self.filled = filled


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
        circ.update()
        return circ
