__author__ = 'ericdennison'

import random
from hhscp.codetest import CodeTest
from StringIO import StringIO

class AreaCalculator(CodeTest):

    htmldescription = """
    This is the demo challenge description
    """
    def __init__(self):
        super(AreaCalculator,self).__init__()
        # Create the stimulus input file
        self.testname = "c05areas"
        s = ""
        pgons = [('square',1),('rectangle',2),('triangle',2),('parallelogram',2),('trapezoid',3),('kite',2),
            (random.choice(['giraffe','monkey','elephant','mouse']),0)]
        random.shuffle(pgons)
        for p,n in pgons:
            s += p + '\n'
            for i in range(0,n):
                s += "{0:.4}\n".format(0.1+random.random()*100)
        s += "none\n"
        self.infile = StringIO(s)

    def canonicalexample(self):
        return """
choice = None
while choice != "none":
    area = None
    choice = raw_input("Find area of a square, rectangle, triangle, parallelogram, trapezoid or kite (or none)? ")
    if choice == "square":
        base = float(raw_input("What is the side length? "))
        area = base**2
    elif choice in ["rectangle", "parallelogram"]:
        base = float(raw_input("What is the base length? "))
        height = float(raw_input("What is the height? "))
        area = base*height
    elif choice == "triangle":
        base = float(raw_input("What is the base length? "))
        height = float(raw_input("What is the height? "))
        area = 0.5*base*height
    elif choice == "trapezoid":
        base1 = float(raw_input("What is one base length? "))
        base2 = float(raw_input("What is another base length? "))
        height = float(raw_input("What is the height? "))
        area = height*(base1+base2)/2.0
    elif choice == "kite":
        diag1 = float(raw_input("What is one diagonal length? "))
        diag2 = float(raw_input("What is another diagonal length? "))
        area = diag1*diag2/2.0
    elif choice != "none":
        print "I'm sorry: I don't know how to find the area of a {0}!".format(choice)
    if area != None:
        print "The area is {0:.6}".format(area)
"""

    def passes(self):
        return self.aresimilar()