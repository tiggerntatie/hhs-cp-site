__author__ = 'ericdennison'

from random import randint
from hhscp.codetest import CodeTest
from StringIO import StringIO

class MultiplicationTable(CodeTest):

    htmldescription = """
    This is the demo challenge description
    """
    def __init__(self):
        super(MultiplicationTable,self).__init__()
        # Create the stimulus input file
        self.testname = "c12multiplicationtable"
        self.width = randint(5,15)
        self.height = randint(5,15)
        self.infile = StringIO("{0}\n{1}\n".format(self.width, self.height))

    def canonicalexample(self):
        return """
width = input("Width of multiplication table: ")
height = input("Height of multiplication table: ")
print ""
# Print the table.
for i in range(1, height + 1):
    for j in range(1, width + 1):
        print "{0:>3}".format(i*j),
    print "" 
"""

    def passes(self):
        return self.aresimilar()