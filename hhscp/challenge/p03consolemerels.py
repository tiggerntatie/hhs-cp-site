__author__ = 'ericdennison'

from hhscp.codetest import CodeTest
from StringIO import StringIO

class ConsoleMerels(CodeTest):

    htmldescription = """
    The third project assignment. Implement ancient Roman Merels.
    """
    def __init__(self):
        super(ConsoleMerels,self).__init__()
        # Create the stimulus input file
        self.testname = "p03consolemerels"
        self.infile = StringIO() # No input text
        self.istestable = False

    def canonicalexample(self):
        return ""