__author__ = 'ericdennison'

tests = {
    'c01hello':'HelloWorld',
    'c02hello':'HelloFriend',
    'c03pforpi':'PiEstimate',
    'c04fizzbuzz':'FizzBuzz',
    'c05areas':'AreaCalculator',
    'c06characterdistribution':'CharDist',
    'c07stringjumble':'StrJumble',
    'c08classdict':'AreaClass',
    'c09exceptions':'Exceptions',
    'c12multiplicationtable':'MultiplicationTable',
    'p01tkcalculator':'TkCalculator',
    'p02conwayslife' : 'ConwaysLife',
    'p03consolemerels' : 'ConsoleMerels',
    'p04pygamemerels' : 'PygameMerels'
}

def gettest(modulename):
    """
    Accept challenge/test name and return a reference to its constructor
    """
    mod =  __import__(modulename, globals(), locals(), [tests[modulename]])
    return getattr(mod, tests[modulename])

def gettests(path, includeempty=True):
    """
    Accept a directory where saved test results may be found, return a
    dictionary of all codetests in testname:instance format.
    """
    alltestslist = [gettest(name)() for name in tests]
    [test.loadstate(path) for test in alltestslist]
    if not includeempty:
        alltestslist = filter(lambda x: len(x.testcode) > 0, alltestslist)
    alltests = dict([(x.testname,x) for x in alltestslist])
    return alltests
