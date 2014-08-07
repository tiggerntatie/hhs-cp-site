__author__ = 'ericdennison'

from random import randint
from hhscp.codetest import CodeTest
from io import StringIO

class PiEstimate(CodeTest):

    htmldescription = """
    This is the demo challenge description
    """
    def __init__(self):
        super(PiEstimate,self).__init__()
        # Create the stimulus input file
        self.testname = "c03pforpi"
        self.terms = randint(10,100)
        self.sigfigs = randint(6,15)
        self.infile = StringIO("{0}\n{1}\n".format(self.terms, self.sigfigs))

    def canonicalexample(self):
        return """
n = int(input("I will estimate pi. How many terms should I use? "))
sigfigs = int(input("How many sig figs should I use in the result? "))
pi = 4*sum([((-1)**k)/(2.0*k+1) for k in range(0,n)])
print("The approximate value of pi is {0:.{precision}}".format(pi,precision=sigfigs))
"""

    def passes(self):
        return self.aresimilar()