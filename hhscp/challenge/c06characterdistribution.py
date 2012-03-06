__author__ = 'ericdennison'

import random
from hhscp.codetest import CodeTest
from StringIO import StringIO

class CharDist(CodeTest):

    htmldescription = """
    This is the demo challenge description
    """
    def __init__(self):
        super(CharDist,self).__init__()
        # Create the stimulus input file
        self.testname = "c06characterdistribution"
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
import string

originaltext = raw_input("Please enter a string of text (the bigger the better): ")
text = originaltext.lower()
counts = [text.count(c) for c in string.letters]  # build a list with character counts for a, b, c, etc..
pairs = zip(counts,string.letters)  # zip the counts together with the characters
pairs.sort(reverse=True)   # sort the zipped list of pairs so that biggest counts are first
charbars = [char*count for char,count in pairs]  # build a list of strings with correct # of chars
charbars = filter(lambda x : len(x)>0, charbars) # discard empty strings from the list
print ('The distribution of characters in "{0}" is: '.format(originaltext))
meta = []
# preparing to build a list of lists of charbars with same length
for bar in charbars:
    if len(meta) == 0 or len(bar) < len(meta[-1][0]):
        meta.append([bar])  # create new entry with a list of bar
    else:
        meta[-1].append(bar) # add this bar to the last list of bars
for charbarset in meta:
    charbarset.sort()
    for charbar in charbarset:
        print(charbar)
"""

    def passes(self):
        return self.aresimilar()