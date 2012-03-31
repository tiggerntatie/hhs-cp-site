__author__ = 'ericdennison'


class Square(object):
    def __init__(self, side = 1.0):
        self.b = side

    def area(self):
        return self.b**2

    def _userinputgeneric(self, member, paramname):
        inp = raw_input("What is the {0}? ".format(paramname))
        try:
            self.__dict__[member] = abs(float(inp))
        except ValueError:
            print("Sorry: {0} is not a valid {1}.".format(inp, paramname))
            raise

    def userinput(self):
        self._userinputgeneric('b','side length')

    def useroutput(self):
        print("The area is {0:.6}.".format(self.area()))

class Rectangle(Square):
    def __init__(self, base = 1.0, height = 1.0):
        self.b = base
        self.h = height

    def area(self):
        return self.b*self.h

    def userinput(self):
        self._userinputgeneric('b','base length')
        self._userinputgeneric('h','height')

class Parallelogram(Rectangle):
    pass

class Triangle(Rectangle):

    def area(self):
        return 0.5*self.b*self.h

class Trapezoid(Rectangle):

    def __init__(self, base1 = 1.0, base2 = 1.0, height = 1.0):
        self.b = base1
        self.b2 = base2
        self.h = height

    def area(self):
        return self.h*(self.b+self.b2)/2.0

    def userinput(self):
        self._userinputgeneric('b','base length')
        self._userinputgeneric('b2','second base length')
        self._userinputgeneric('h','height')

class Kite(Square):

    def __init__(self, diam1 = 1.0, diam2 = 1.0):
        self.d1 = diam1
        self.d2 = diam2

    def area(self):
        return self.d1*self.d2/2.0

    def userinput(self):
        self._userinputgeneric('d1','diagonal length')
        self._userinputgeneric('d2','other diagonal length')



# handlers dictionary relates user command to objects to use
handlers = {
            'trapezoid': Trapezoid(),
            'square':Square(),
            'rectangle':Rectangle(),
            'parallelogram':Parallelogram(),
            'triangle':Triangle(),
            'kite':Kite()}


choice = None
while choice != "none":
    choice = raw_input("Find area of a square, rectangle, triangle, parallelogram, trapezoid or kite (or none)? ")
    obj = handlers.get(choice,None)  # retrieve an object of the correct type, or None if not recognized
    if obj:
        try:
            obj.userinput() # Retrieve values
            obj.useroutput() # What is the area
        except ValueError:
            print("Please try again!")
    elif choice != "none":
        print "I'm sorry: I don't know how to find the area of a {0}!".format(choice)

