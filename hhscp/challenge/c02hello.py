__author__ = 'ericdennison'

from random import randint
from hhscp.codetest import CodeTest
from StringIO import StringIO

class HelloFriend(CodeTest):

    htmldescription = """
    This is the demo challenge description
    """
    def __init__(self):
        super(HelloFriend,self).__init__()
        # Create the stimulus input file
        self.testname = "c02hello"
        self.names = ['Fred', 'Sally', 'Cindy', 'Bob', 'Jim']
        self.nameint = randint(0,4)
        self.age = randint(10,19)
        self.infile = StringIO("{0}\n{1}\n".format(self.names[self.nameint], self.age))

    def canonicalexample(self):
        return """
name = raw_input("Please tell me your name: ")
age = int(raw_input("Please tell me your age: "))
pythonage = 2012-1989
print("Hello, {0}. Python is {1} years older than you are!".format(name, pythonage-age))
"""

    def passes(self):
        return self.aresimilar()