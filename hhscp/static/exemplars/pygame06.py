import pygame
from pygame.locals import *

from pygameapp06 import *

class MyApp(PygameApp):
    """
    Custom version of PygameApp, to display moving circle
    """
    def __init__(self, screensize = (400,400)):
        """
        Application initialization is executed only ONCE!
        """
        super(MyApp,self).__init__(screensize = screensize, title="My Test Application") # call base class initializer
        pygame.key.set_repeat(100)              # allow keys to repeat when held 100 msec
        self.setbackground((220,220,220))       # set a new background color
        self.circ = Circle(self.spritegroup)    # create a default circle

    def handle_event(self, event):
        """
        Override the base class event handler. Based on mouse and keyboard input make adjustments
        to the Circle object or make copies of it.
        """
        if event.type == MOUSEMOTION:
            self.circ.setpos(event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4:                   # scroll UP "button"
                self.circ.setradius(self.circ.radius+1)
            elif event.button == 5:                 # scroll DOWN "button"
                self.circ.setradius(self.circ.radius-1)
            elif event.button == 1:
                newcirc = self.circ.copy()          # copy the circle on button down
                newcirc.setcolor((255,0,0,200))
                newcirc.setthickness(1)
                newcirc.update()                    # force update and display
        elif event.type == KEYDOWN:                 # keyboard
            circpos = self.circ.pos
            if event.key == K_UP:                   # cursor up
                circpos = (circpos[0],circpos[1]-1) # calculate a new position
            elif event.key == K_DOWN: # cursor down
                circpos = (circpos[0],circpos[1]+1) # calculate a new position
            self.circ.setpos(circpos)             # update the position
        else:
            print pygame.event.event_name(event.type)   # view unhandled events on the console

        if event.type in [MOUSEMOTION, MOUSEBUTTONDOWN, KEYDOWN]:
            self.circ.update()                      # force update to our main circle

    def quit(self):
        """
        Override default quit behavior here, if desired
        """
        pass

    def poll(self):
        """
        Override default poll behavior here, if desired
        """
        pass


# Run an instance of MyApp!
myapp = MyApp()
myapp.run(100)   # 100 frames per second!