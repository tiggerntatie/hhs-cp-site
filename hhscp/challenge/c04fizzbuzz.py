__author__ = 'ericdennison'

from random import randint
from hhscp.codetest import CodeTest
from io import StringIO

class FizzBuzz(CodeTest):

    htmldescription = """
    This is the demo challenge description
    """
    def __init__(self):
        super(FizzBuzz,self).__init__()
        # Create the stimulus input file
        self.testname = "c04fizzbuzz"
        self.terms = randint(40,60)
        fizzbuzz = lambda x=9 : randint(3,x)
        self.fizzn = fizzbuzz()
        self.buzzn = fizzbuzz(self.terms//self.fizzn)
        while (self.fizzn == self.buzzn or
            not self.fizzn % self.buzzn  or
            not self.buzzn % self.fizzn):
            self.buzzn = fizzbuzz(self.terms//self.fizzn)
        self.infile = StringIO("{0}\n{1}\n{2}\n".format(self.terms, self.fizzn, self.buzzn))

    def canonicalexample(self):
        return """
maxn = int(input("How many numbers shall we print? "))
fizzn = int(input("For multiples of what number shall we print 'Fizz'? "))
buzzn = int(input("For multiples of what number shall we print 'Buzz'? "))

for n in range(1,maxn+1):
    fizzmultiple = not n % fizzn # % calculates remainder of division - zero if n is multiple of fizzn
    buzzmultiple = not n % buzzn # ditto..
    if fizzmultiple and buzzmultiple:   # check for both, first
        print("FizzBuzz")
    elif fizzmultiple:  # then individuals
        print("Fizz")
    elif buzzmultiple:
        print("Buzz")
    else:
        print(n)
"""

    def passes(self):
        return self.aresimilar()