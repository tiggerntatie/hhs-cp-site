__author__ = 'ericdennison'

from hhscp.codetest import CodeTest
from io import StringIO

class PygamePlatformer(CodeTest):

    htmldescription = """
    The fifth project assignment. Implement platformer sandbox using Pygame.
    """
    def __init__(self):
        super(PygamePlatformer,self).__init__()
        # Create the stimulus input file
        self.testname = "p05pygameplatformer"
        self.infile = StringIO() # No input text
        self.istestable = False

    def canonicalexample(self):
        return ""