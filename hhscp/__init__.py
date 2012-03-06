"""
Hanover High School Computer Programming web applicaton!


Something to try for sandboxing:

del os
>>> sys.modules['os']=None
>>> import os
(will fail, even inside exec)


redirecting output

oldstdout = sys.stdout
>>> sys.stdout = open('testout.txt','w')
>>> exec('print "oh crap"\n',{})
>>> dir(sys.stdout)
>>> sys.stdout.close()


"""

__author__ = 'ericdennison'


from flask import Flask

app = Flask(__name__)

from pages import *

if __name__ == '__main__':
    app.debug = True
    app.run()