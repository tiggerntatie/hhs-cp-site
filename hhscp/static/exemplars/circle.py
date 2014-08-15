import pygame

# Circle class extends Pygame DirtySprite

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
