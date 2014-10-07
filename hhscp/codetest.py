__author__ = 'ericdennison'

from io import StringIO
import sys
import os
import string
import difflib
import re
#import cgi
from flask import url_for
import hhscp.challenge
import tempfile
import subprocess
from hhscp import app

class CodeTest(object):


    def __init__(self):
        self.testname = ''
        self.testcode = ''
        self.infile = StringIO()
        self.outfile = StringIO()
        self.canonicaloutfile = StringIO()
        self.path = ''
        self.istestable = True # set False in child class to skip executing code (for GUI code, etc.)
        self._stateattrs = ['input','canonicaloutput','output','testcode']
        self._stateextensions = ['input','canout','out','py']
        self._stateinfo = list(zip(self._stateextensions,self._stateattrs))
    
        self.htmldescription = """
        This is a default challenge description
        """

    def _runtest(self, testcode):
        """
        run code test and return input and output
        """
        pyfile = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8')  
        #self.testcode = string.translate(testfile.read(),None,'\r') # strip unwanted characters
        safecode = """
import sys
sys.modules['os']=None
sys.modules['subprocess']=None
"""
                
        pyfile.file.write(safecode + testcode + self.postcheck())  # code to execute
        pyfile.file.flush()
        conout = tempfile.SpooledTemporaryFile(max_size=1000, mode='r+')
        conin = tempfile.SpooledTemporaryFile(max_size=1000, mode='r+')
        conin.write(self.infile.getvalue())
        conin.seek(0)
        try:
            subprocess.call(['python3', pyfile.name], stdout=conout, stdin=conin, stderr=conout, timeout=1)
            conout.seek(0)
            output = conout.read()
        except subprocess.TimeoutExpired:
            output = "*** Process timed out: do you have an infinite loop? ***"
        input = self.infile.getvalue()  # hold on to the input
        pyfile.close()
        conout.close()
        conin.close()
        return input, output[:100000] # limit the size of output

    def _pretest(self, infile, outfile):
        self.savein, self.saveout = sys.stdin, sys.stdout
        sys.stdin, sys.stdout = infile, outfile

    def _posttest(self):
        self.infile.seek(0)
        self.input = self.infile.getvalue()
        self.output = self.outfile.getvalue()
        sys.stdin, sys.stdout = self.savein, self.saveout

    def runtest(self,testfile):
        self.testcode = str(testfile.read(), 'utf-8').replace('\r','') # strip unwanted characters
        if self.istestable:
            self.input, self.output = self._runtest(self.testcode)
        else:
            self.input = self.output = ""
            
    def testcanonicalexample(self):
        if self.istestable:
            input, self.canonicaloutput = self._runtest(self.canonicalexample())
        else:
            self.canonicaloutput = ""

    def savestate(self, path=''):
        for typ, data in self._stateinfo:
            f = open(os.path.join(path, self.testname+'.'+typ), 'w+', encoding='utf-8')
            f.write(getattr(self, data))
            f.close()

    def loadstate(self, path=''):
        try:
            for typ, data in self._stateinfo:
                f = open(os.path.join(path, self.testname+'.'+typ), 'r', encoding='utf-8')
                setattr(self, data, f.read())
                f.close()
        except IOError or UnicodeDecodeError:
            for data in self._stateattrs:
                setattr(self, data, '')
            #[setattr(self,data,'') for data in self._stateattrs]
        except UnicodeDecodeError:
            self.testcode = "NO VALID PYTHON FOUND!"

    def canonicalexample(self):
        """
        Method implements functionality that is expected from uploaded user code.
        To be overridden in child class implementations.
        """
        print("Empty")

    def postcheck(self):
        """
        Method may provide some optional interaction with the user supplied code (e.g. instantiating
        or calling user classes/methods and printing the result of those). This method is executed
        after calling the user supplied code, but before capturing the final console output.
        """
        return ""

    def passes(self):
        """
        Determine if submission meets requirement for passing
        If istestable is false, it always passes
        """
        return not self.istestable or self.aresame()

    def aresimilar(self):
        """
        Determine if canonical and test output are similar to each other.
        """
        return re.sub("\s*", "", self.output) == re.sub("\s*", "", self.canonicaloutput)

    def aresame(self):
        """
        Determine if canonical and test output are identical to each other.
        """
        return self.output == self.canonicaloutput

    def userchallengeurl(self, username):
        """
        Return url to the specific user's version of the challenge
        """
        return url_for('site_userchallenge', username=username, challengename=self.testname)

    def userchallengesubmiturl(self, username):
        """
        Return url to the specific user's version of the challenge
        """
        return url_for('site_userchallengesubmit', username=username, challengename=self.testname)

    def submitted(self):
        """
        Return True if there is user code
        """
        return self.testcode != ""

    def testcodehtml(self):
        """
        Return html escaped testcode
        """
        return self.testcode

    def outputhtml(self):
        """
        Return html escaped output
        """
        return self.output

    def inputhtml(self):
        """
        Return html escaped input
        """
        return self.input

    def canonicaloutputhtml(self):
        """
        Return html escaped canonicaloutput
        """
        return self.canonicaloutput

    def diff(self):
        """
        Return html of diff between outputs
        """
        d = difflib.Differ()
        retval = ""
        for line in d.compare(self.canonicaloutput.splitlines(), self.output.splitlines()):
            retval += line + '\n'
        return retval

if __name__ == '__main__':
    pass