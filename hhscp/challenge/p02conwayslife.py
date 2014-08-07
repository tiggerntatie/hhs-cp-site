__author__ = 'ericdennison'

from hhscp.codetest import CodeTest
from io import StringIO

class ConwaysLife(CodeTest):

    htmldescription = """
    The second project assignment. Implement Conway's Life.
    """
    def __init__(self):
        super(ConwaysLife,self).__init__()
        # Create the stimulus input file
        self.testname = "p02conwayslife"
        self.infile = StringIO() # No input text
        self.istestable = False

    def canonicalexample(self):
        return ""