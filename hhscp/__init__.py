"""
Hanover High School Computer Programming web applicaton!

"""

__author__ = 'ericdennison'

import sys


#sys.path.append('./static/exemplars')
sys.path.append('./hhscp/static/exemplars')

from flask import Flask
from hhscp.reverseproxied import ReverseProxied

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

from hhscp.pages import *

#if __name__ == '__main__':
#    app.debug = True
#    app.run()
