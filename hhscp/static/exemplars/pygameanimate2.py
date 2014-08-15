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
            pygame.display.update()
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


# Now make your own application, based on PygameApp

class MyApp(PygameApp):
    """
    Custom version of PygameApp, to display moving circle
    """
    def __init__(self, screensize = (600,300), velocity = (240, 60)):
        super().__init__(screensize=screensize) # call base class initializer
        # super().__init__(fullscreen = True)   # uncomment to try full screen!
        self.color = pygame.Color('white')
        self.radius = 50
        self.linewidth = 1
        self.xmin = self.radius
        self.xmax = self.screensize[0] - self.radius
        self.ymin = self.radius
        self.ymax = self.screensize[1] - self.radius
        self.position = [self.xmin, self.ymin]
        self.velocity = list(velocity)


    def poll(self):
        """
        Overrides the empty poll function in PygameApp
        """
        super().poll()                              # call super class poll function
        
        # compute a new position for the circle based on old position and velocity 
        self.position = [p + v/self.fps for p,v in zip(self.position, self.velocity)] 
                                                    # v/FPS computes pixels/frame instead of pixels/second
                                                    # resulting position is a tuple of floats!
        
        # check to see if the circle is outside the margin
        if ((self.position[0] > self.xmax and self.velocity[0] > 0) or          
            (self.position[0] < self.xmin and self.velocity[0] < 0)):
            self.velocity[0] *= -1                                   
    
        if ((self.position[1] > self.ymax and self.velocity[1] > 0) or          
            (self.position[1] < self.ymin and self.velocity[1] < 0)):          
            self.velocity[1] *= -1                                   

        self.erase()                                # erase the display surface
        pygame.draw.circle(self.display, 
                           self.color,
                           [int(x) for x in self.position],
                           self.radius, 
                           self.linewidth)          # draw a circle
        
    def handle_event(self, event):
        """
        Overrides the empty handle_event function in PygameApp
        """
        # handle a single event .. look for the 'q' key to quit
        if event.type == KEYDOWN and event.unicode == 'q':
            return False
        print(event)                                # otherwise, print the event
        return True

# MyApp is created (instantiated) and executed with the run member function!
myapp = MyApp((400,200))
myapp.run()
