__author__ = 'ericdennison'

import random
from hhscp.codetest import CodeTest
from io import StringIO

class AreaClass(CodeTest):

    htmldescription = """
    This is the demo challenge description
    """
    def __init__(self):
        super(AreaClass,self).__init__()
        # Create the stimulus input file
        self.testname = "c08classdict"
        s = ""
        endpgons = [('square',1),('rectangle',2),('triangle',2),('parallelogram',2),('trapezoid',3),('kite',2)]
        pgons = [('square',1),('rectangle',2),('triangle',2),('parallelogram',2),('trapezoid',3),('kite',2),
            (random.choice(['giraffe','monkey','elephant','mouse']),0)]
        random.shuffle(pgons)
        for p,n in pgons:
            s += p + '\n'
            for i in range(0,n):
                s += "{0:.4}\n".format(0.1+random.random()*100)
        s += "none\n"
        for p,n in endpgons:
            for i in range(0,n):
                s += "{0:.4}\n".format(0.1+random.random()*100)
        self.infile = StringIO(s)

    def canonicalexample(self):
        return """
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
        self.b = base
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
        self.b = base1
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
handlers = {'square':Square(),
            'rectangle':Rectangle(),
            'parallelogram':Parallelogram(),
            'triangle':Triangle(),
            'trapezoid':Trapezoid(),
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
"""

    def postcheck(self):
        return """
print("\\nExtended object testing...")
objs = [Square(), Rectangle(), Triangle(), Parallelogram(), Trapezoid(), Kite()]
for obj in objs:
    obj.userinput()
    obj.useroutput()
    print(obj.area())
"""


    def passes(self):
        return self.aresimilar()