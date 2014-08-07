__author__ = 'ericdennison'

from hhscp.codetest import CodeTest
from io import StringIO

class PygameMerels(CodeTest):

    htmldescription = """
    The third project assignment. Implement ancient Roman Merels using Pygame.
    """
    def __init__(self):
        super(PygameMerels,self).__init__()
        # Create the stimulus input file
        self.testname = "p04pygamemerels"
        self.infile = StringIO() # No input text
        self.istestable = False

    def canonicalexample(self):
        return ""