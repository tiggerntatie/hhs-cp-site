import pygame
from pygame.locals import *

from pygameapp import PygameApp
from circle import Circle

class MyCircle(Circle):
    """
    Customized update function accepts a view offset tuple
    """
    def __init__(self, *groups):
        self.offset = (0,0)
        super().__init__(groups)

    def update(self, *args):
        super(MyCircle,self).update(args)
        if len(args) == 1:
            self.offset = args[0]
        self.rect.move_ip(self.offset)

    def copy(self):
        """
        Make a copy of the circle and return it
        """
        circ = MyCircle(self.groups())    # make a new circle, using the same groups that this one has
        circ.setpos(self.pos)           # give it the same parameters as this one
        circ.setradius(self.radius)
        circ.setcolor(self.color)
        circ.setthickness(self.thickness)
        circ.setfilled(self.filled)
        circ.offset = self.offset
        circ.update()
        return circ


class ConwayApp(PygameApp):
    """
    Custom version of PygameApp, to run Conway's Game of Life. Grid is fixed at 80x80 cells, 10 pixels per cell.
    """
    def __init__(self, screensize = (600,600)):
        """
        Application initialization is executed only ONCE!
        """
        super().__init__(screensize = screensize, title="Conway's Life") # call base class initializer
        pygame.key.set_repeat(100)              # allow keys to repeat when held 100 msec
        self.offset = (0,0)     # relative position of the viewport
        self.cellsize = 4
        self.cellswide = self.screensize[0] / self.cellsize
        self.cellshigh = self.screensize[1] / self.cellsize
        self.cellboard = {}     # an empty map for storing cells
        self.mousedown = False  # keep track of the button state
        self.mousepos = (0,0)   # keep track of the mouse position
        self.setbackgroundcolor((220,220,220))       # set a new background color
        self.circ = MyCircle()                    # create a default circle, but not in a group yet
        self.circ.setfilled(True)
        self.circ.setradius(self.cellsize//2)
        self.circ.setcolor((20,20,200,150))

    def handle_event(self, event):
        """
        Override the base class event handler. Based on mouse and keyboard input make adjustments
        to the Circle object or make copies of it.
        """
        if event.type == MOUSEMOTION:
            self.mousepos = tuple([x[0]+x[1] for x in zip(event.pos, event.rel)])
        if event.type == MOUSEBUTTONDOWN:
            self.mousedown = True
        elif event.type == MOUSEBUTTONUP:
            self.mousedown = False
        if (event.type == MOUSEMOTION and self.mousedown) or (event.type == MOUSEBUTTONDOWN):
            logicalcoordinates = self.logicalcoordinates(self.mousepos)         # x,y coordinates of the mouse
            if logicalcoordinates not in self.cellboard:                  # if it isn't already created..
                self.cellboard[logicalcoordinates] = self.newcircle(logicalcoordinates)  # add it to the playing board
        elif event.type == KEYDOWN:                 # keyboard
            if event.key == K_UP:                   # cursor up
                self.offset = (self.offset[0],self.offset[1]+self.cellsize*5) # calculate a new position
            elif event.key == K_DOWN:               # cursor down
                self.offset = (self.offset[0],self.offset[1]-self.cellsize*5) # calculate a new position
            elif event.key == K_RIGHT:              # cursor right
                self.offset = (self.offset[0]-self.cellsize*5,self.offset[1]) # calculate a new position
            elif event.key == K_LEFT:               # cursor left
                self.offset = (self.offset[0]+self.cellsize*5,self.offset[1]) # calculate a new position
            self.spritegroup.update(self.offset)               # update the position
        return True
        #print event   # view events on the console

    def quit(self):
        """
        Override default quit behavior here, if desired
        """
        pass

    def poll(self):
        """
        Perform the rules of Life on each element on the grid that might be affected by constructing
        a set of all points within range of known points
        """
        points = set(self.cellboard)        # will be a set of all keys
        newpoints = set()
        for point in points:
            newpoints.update(set(self.neighbors(point)))    # build a set of all neighboring points
        points.update(newpoints)            # merge with the original list
        newcellboard = {}                   # prepare to build a new cell board
        for point in points:                # for all of the expanded list
            neighborcount = self.neighborcount(point)
            if point in self.cellboard:
                thiscirc = self.cellboard[point]                    # get the circle that's h
                if neighborcount == 2 or neighborcount == 3:
                    thiscirc.setcolor(self.circ.color)
                    thiscirc.update()
                    newcellboard[point] = thiscirc                  # YES: we need this for the new board
                else:
                    self.spritegroup.remove(thiscirc)               # NO: pull it from the display list
            elif neighborcount == 3:                                # empty with three neighbors
                newcellboard[point] = self.newcircle(point)
        self.cellboard = newcellboard                                   # swap in the new map


    def screencoordinates(self, logicalxy):
        """
        Convert logical x,y coordinates to screen coordinates
        """
        return tuple(map(lambda x: x*self.cellsize, logicalxy))

    def logicalcoordinates(self, screenxy):
        """
        Convert screen x,y coordinates to logical coordinates
        """
        adjusted = (screenxy[0]-self.offset[0],screenxy[1]-self.offset[1])
        return tuple(map(lambda x: (x+self.cellsize//2)//self.cellsize, adjusted))

    def newcircle(self, logicalxy):
        """
        Generate a new circle at the given logical location and add it to the display list
        """
        newcirc = self.circ.copy()
        newcirc.setpos(self.screencoordinates(logicalxy))
        newcirc.setcolor((255,0,0))
        newcirc.offset = self.offset
        newcirc.update()
        self.spritegroup.add(newcirc)
        return newcirc

    def neighbors(self, logicalxy):
        """
        For a given logical position, return a list of neighboring coordinate tuples
        """
        retval = []
        for x in range(logicalxy[0]-1, logicalxy[0]+2):
            for y in range(logicalxy[1]-1, logicalxy[1]+2):
                if (x,y) != logicalxy:
                    retval.append((x,y))
        return retval

    def neighborcount(self, logicalxy):
        """
        For a given logical position, return total living neighbors
        """
        total = 0
        for x,y in self.neighbors(logicalxy):
            if (x,y) in self.cellboard:
                total += 1
        return total

# Run an instance of MyApp!
myapp = ConwayApp()
myapp.run(10)   # ? frames per second!
