__author__ = 'ericdennison'

from hhscp import app
from hhscp.events import *
from hhscp.users import User, Users
from flask import render_template
from flask import request
from werkzeug import secure_filename
from flask import redirect
import inspect
import sys



@app.route('/test')
def site_test():
    savestdin = sys.stdin
    savestdout = sys.stdout
    sys.stdin = open('./stdin/test.txt','r')
    sys.stdout = open('./stdout/test.txt','w')
    exec 'inp = raw_input()\nprint "hello, %s" % (inp)'
    sys.stdout.close()
    sys.stdin.close()
    return open('./stdout/test.txt','r').read()

@app.route('/calendar')
def site_calendar():
    c = Calendar()
    return render_template('calendar.html', title='Computer Programming Course Calendar', weeks=c.weeks)

@app.route('/')
def site_main():
#    return "this is the main"
#    return str(os.listdir('.'))
    return render_template('main.html', title='HHS - Computer Programming')

@app.route('/assignment/<short_name>')
def site_assignment(short_name):
    c = Calendar()
    event = c.assignments.nameDict[short_name]
    return render_template('assignments/' + short_name + '.html',
        title=event.name,
        builtins=__builtins__)


@app.route('/user/<name>')
def site_user(name):
    u = User(name)
    return render_template('user.html', title=u.longname, user=u )

@app.route('/users')
def site_users():
    u = Users()
    return render_template('users.html', title='Computer Programming Users', users=u)


@app.route('/userchallengesubmit/<username>/<challengename>', methods=['GET', 'POST'])
def site_userchallengesubmit(username, challengename):
    u = User(username)
    c = u.challenge(challengename)
    if request.method == 'POST':
        file = request.files['file']
        if file and request.form['pass'] == u.password:
            c.testcanonicalexample()
            c.runtest(file)
            c.savestate(u.datapath)
    return redirect(c.userchallengeurl(username))


@app.route('/userchallenge/<username>/<challengename>')
def site_userchallenge(username, challengename):
    u = User(username)
    c = u.challenge(challengename)
    return render_template('userchallenge.html', title=u.longname+' - '+c.testname, user=u, challenge=c)

@app.route('/userchallenge/download/<username>/<challengename>')
def site_userchallengedownload(username, challengename):
    u = User(username)
    c = u.challenge(challengename)
    rv = app.make_response(c.testcode)
    rv.headers.add_header('Content-Disposition: attachment;', 'filename=' + u.shortname + c.testname + '.py')
    rv.mimetype = 'text/plain'
    return rv
