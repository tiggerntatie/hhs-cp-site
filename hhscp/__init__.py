"""
Hanover High School Computer Programming web applicaton!

Edit test TWO (github)

"""

__author__ = 'ericdennison'

import sys

#sys.path.append('./static/exemplars')
sys.path.append('./hhscp/static/exemplars')

from flask import Flask

app = Flask(__name__)

from hhscp.pages import *

if __name__ == '__main__':
    app.debug = True
    app.run()