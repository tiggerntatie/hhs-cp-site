__author__ = 'ericdennison'

import csv
import os, os.path
from hhscp import app
from hhscp.events import *
from hhscp.challenge import *
from flask import session
import hashlib

class UserException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

defaultsecretpath = './hhscp/data/cookiekey'
USERSFILE = './hhscp/data/users.csv'
defaultusersdata = './hhscp/userdata/'

ADMIN = 'admin'
ADMIN_LONG = 'Administrator'

try:
    app.secret_key = open(defaultsecretpath).read()
except:
    app.secret_key = b"This is a secret key!"
    

class Users(object):

    def __init__(self, usersfile=USERSFILE):
        self.usersfile = usersfile
        if not os.path.isfile(usersfile):
            adminuser = [ADMIN, ADMIN_LONG, '']
            csv.writer(open(self.usersfile,'w')).writerow(adminuser)
        self.getusers()
        
    def getusers(self):
        self.userslist = list(csv.reader(open(self.usersfile,'r'), skipinitialspace=True))
        self.unames, self.fullnames, self.passhashes = zip(*self.userslist)
            
    def update(self, user):
        self.getusers()
        x = self.unames.index(user.shortname)
        self.fullnames = list(self.fullnames)
        self.fullnames[x] = user.longname
        self.passhashes = list(self.passhashes)
        self.passhashes[x] = user.passhash
        self.userslist = zip(self.unames, self.fullnames, self.passhashes)
        csv.writer(open(self.usersfile,'w')).writerows(self.userslist)

    def logout(self):
        session['passhash'] = None
        session['admin'] = None

class User(object):

    def __init__(self,shortname,usersfile=USERSFILE,usersdata=defaultusersdata):
        """
        Stub
        """
        self.users = Users(usersfile)
        if not shortname in self.users.unames:
            raise UserException('User %s not found' % shortname)
        x = self.users.unames.index(shortname)
        self.shortname = shortname
        self.longname = self.users.fullnames[x]
        self.passhash = self.users.passhashes[x]
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
    
    def authenticated(self):
        return 'passhash' in session and session['passhash'] == self.passhash
    
    def isadminsession(self):
        # Returns TRUE if the administrator is logged in 
        return 'admin' in session and session['admin']
    
    def hashpass(self, password):
        return hashlib.sha512(bytes(password,'utf-8')).hexdigest()
    
    def setpassword(self, password):
        self.passhash = self.hashpass(password)
        self.users.update(self)
        
    def login(self, password):
        session['passhash'] = self.hashpass(password)
        if self.shortname == ADMIN:
            session['admin'] = True
        else:
            session['admin'] = None

        