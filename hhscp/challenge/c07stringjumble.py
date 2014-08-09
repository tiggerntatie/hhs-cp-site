__author__ = 'ericdennison'

import random
from hhscp.codetest import CodeTest
from io import StringIO

class StrJumble(CodeTest):

    htmldescription = """
    This is the demo challenge description
    """
    def __init__(self):
        super(StrJumble,self).__init__()
        # Create the stimulus input file
        self.testname = "c07stringjumble"
        self.samplestrings = ["How now? A rat? Dead, for a ducat, dead!",
                              "Done to death by slanderous tongue",
                              "Why then tonight let us assay our plot",
                              "Thou art a votary to fond desire",
                              "Some Cupid kills with arrows, some with traps",
                                "Be not afraid of greatness",
                                "Lord, what fools these mortals be",
                                "Our remedies oft in ourselves do lie",
                                "I go, and it is done; the bell invites me"]

        s = random.choice(self.samplestrings)
        self.infile = StringIO(s)

    def canonicalexample(self):
        return """
rawtext = input("Please enter a string of text (the bigger the better): ")

allreversed = rawtext[::-1]
allwords = rawtext.split()
allwordsinreverse = allwords[::-1]
allwordsreversed = [word[::-1] for word in allwords]

print ('You entered "{0}". Now jumble it: '.format(rawtext))
print(allreversed)
print(' '.join(allwordsinreverse))
print(' '.join(allwordsreversed))
"""

    def passes(self):
        return self.aresimilar()