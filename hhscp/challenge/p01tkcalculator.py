__author__ = 'ericdennison'

from hhscp.codetest import CodeTest
from StringIO import StringIO

class TkCalculator(CodeTest):

    htmldescription = """
    The first challenge in the programming course
    """
    def __init__(self):
        super(TkCalculator,self).__init__()
        # Create the stimulus input file
        self.testname = "p01tkcalculator"
        self.infile = StringIO() # No input text
        self.istestable = False

    def canonicalexample(self):
        return ""