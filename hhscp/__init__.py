"""
Hanover High School Computer Programming web applicaton!



"""

__author__ = 'ericdennison'


from flask import Flask

app = Flask(__name__)

from pages import *

if __name__ == '__main__':
    app.debug = True
    app.run()