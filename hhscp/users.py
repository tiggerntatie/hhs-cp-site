__author__ = 'ericdennison'

import csv
import os
from hhscp.events import *
from hhscp.challenge import *

class UserException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

defaultuserspath = './hhscp/data/users.csv'
defaultusersdata = './hhscp/userdata/'

class Users(object):

    def __init__(self, usersfile=defaultuserspath):
        self.userslist = list(csv.reader(open(usersfile,'r'), skipinitialspace=True))
        self.unames, self.fullnames, self.passwords = zip(*self.userslist)

class User(object):

    def __init__(self,shortname,usersfile=defaultuserspath,usersdata=defaultusersdata):
        """
        Stub
        """
        users = Users(usersfile)
        if not shortname in users.unames:
            raise UserException('User %s not found' % shortname)
        x = users.unames.index(shortname)
        self.shortname = shortname
        self.longname = users.fullnames[x]
        self.password = users.passwords[x]
        self.datapath = os.path.join(usersdata,shortname)
        try:
            os.makedirs(self.datapath, mode=0o751)
        except:
            pass
        self.calevents = Calendar().assignments.events
        shortnames = [a.shortname for a in self.calevents]
        #self.challenges = filter(lambda test: test.testname in shortnames, gettests(self.datapath))
        self.challenges = gettests(self.datapath)

    def challenge(self, challengename):
        c = gettest(challengename)()
        c.loadstate(self.datapath)
        return c