__author__ = 'ericdennison'

from random import randint
from hhscp.codetest import CodeTest
from io import StringIO

class HelloWorld(CodeTest):

    def __init__(self):
        super(HelloWorld,self).__init__()
        # Create the stimulus input file
        self.testname = "c01hello"
        self.infile = StringIO("") # No input text
        self.htmldescription = """
The first challenge in the programming course
"""


    def canonicalexample(self):
        return """
print ("Hello, world!")
"""