__author__ = 'ericdennison'


class Square(object):
    def __init__(self, side = 1.0):
        self.b = side

    def area(self):
        return self.b**2

    def userinput(self):
        self.b = abs(float(raw_input("What is the side length? ")))

    def useroutput(self):
        print("The area is {0:.6}.".format(self.area()))

class Rectangle(Square):
    def __init__(self, base = 1.0, height = 1.0):
        super(Rectangle,self).__init__(base)
        self.h = height

    def area(self):
        return self.b*self.h

    def userinput(self):
        self.b = abs(float(raw_input("What is the base length? ")))
        self.h = abs(float(raw_input("What is the height? ")))

class Parallelogram(Rectangle):
    pass

class Triangle(Rectangle):

    def area(self):
        return 0.5*self.b*self.h

class Trapezoid(Rectangle):

    def __init__(self, base1 = 1.0, base2 = 1.0, height = 1.0):
        super(Trapezoid, self).__init__(base1)
        self.b2 = base2
        self.h = height

    def area(self):
        return self.h*(self.b+self.b2)/2.0

    def userinput(self):
        self.b = abs(float(raw_input("What is one base length? ")))
        self.b2 = abs(float(raw_input("What is another base length? ")))
        self.h = abs(float(raw_input("What is the height? ")))

class Kite(Square):

    def __init__(self, diam1 = 1.0, diam2 = 1.0):
        self.d1 = diam1
        self.d2 = diam2

    def area(self):
        return self.d1*self.d2/2.0

    def userinput(self):
        self.d1 = abs(float(raw_input("What is one diagonal length? ")))
        self.d2 = abs(float(raw_input("What is another diagonal length? ")))



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
        obj.userinput() # Retrieve values
        obj.useroutput() # What is the area
    elif choice != "none":
        print "I'm sorry: I don't know how to find the area of a {0}!".format(choice)

