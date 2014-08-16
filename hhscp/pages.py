__author__ = 'ericdennison'

from hhscp import app
from hhscp.events import *
from hhscp.users import User, Users, ADMIN, USERSFILE
from flask import render_template
from flask import request, session
from flask import redirect
import inspect
import sys
import datetime


@app.route('/calendar')
def site_calendar():
    c = Calendar()
    return render_template('calendar.html', title='Computer Programming Course Calendar', weeks=c.weeks)

@app.route('/')
def site_main():
    return render_template('main.html', title='HHS - Computer Programming')

@app.route('/assignment/<short_name>')
def site_assignment(short_name):
    c = Calendar(True)          # allow all assignments
    event = c.assignments.nameDict[short_name]
    return render_template('assignments/' + short_name + '.html',
        title=event.name,
        datetime=datetime,
        builtins=__builtins__)


@app.route('/user/<name>')
def site_user(name):
    u = User(name)
    if u.isadminsession() or u.authenticated():
        return render_template('user.html', title=u.longname, user=u )
    elif not u.passhash:
        return redirect(url_for('site_getnewpass', name=name))
    elif not u.authenticated():
        return redirect(url_for('site_authenticate', name=name))
    else:
        return redirect(url_for('site_users'))
    
@app.route('/logout')
def site_logout():
    u = Users()
    u.logout()
    return redirect(url_for('site_users'))

@app.route('/getnewpass/<name>')
def site_getnewpass(name):
    u = User(name)
    if not u.passhash or u.authenticated():
        return render_template('setpass.html', user=u)
    else:
        redirect(url_for('site_authenticate', name=name))
        
@app.route('/getnewpasssubmit/<name>', methods=['POST'])
def site_getnewpasssubmit(name):
    u = User(name)
    if (not u.passhash or u.authenticated()) and request.form['pass1'] == request.form['pass2']:
        u.setpassword(request.form['pass1'])
    return redirect(url_for('site_authenticate', name=name))

@app.route('/authenticate/<name>')
def site_authenticate(name):
    u = User(name)
    return render_template('authenticate.html', user=u)

@app.route('/authenticatesubmit/<name>', methods=['POST'])
def site_authenticatesubmit(name):
    u = User(name)
    if request.method == 'POST':
        u.login(request.form['pass'])
    return redirect(url_for('site_user', name=name))

@app.route('/users')
def site_users():
    u = Users()
    return render_template('users.html', title='Computer Programming Users', users=u)


@app.route('/userchallengesubmit/<username>/<challengename>', methods=['POST'])
def site_userchallengesubmit(username, challengename):
    u = User(username)
    c = u.challenge(challengename)
    if not u.authenticated():
        return redirect(url_for('site_authenticate', name=username))
    if request.method == 'POST':
        file = request.files['file']
        if file:
            c.testcanonicalexample()
            c.runtest(file)
            c.savestate(u.datapath)
    return redirect(c.userchallengeurl(username))


@app.route('/userchallenge/<username>/<challengename>')
def site_userchallenge(username, challengename):
    u = User(username)
    c = u.challenge(challengename)
    if not u.authenticated() and not u.isadminsession():
        return redirect(url_for('site_authenticate', name=username))
    return render_template('userchallenge.html', title=u.longname+' - '+c.testname, user=u, challenge=c)

@app.route('/userchallenge/download/<username>/<challengename>')
def site_userchallengedownload(username, challengename):
    u = User(username)
    if not u.authenticated() and not u.isadminsession():
        return redirect(url_for('site_authenticate', name=username))
    c = u.challenge(challengename)
    rv = app.make_response(c.testcode)
    #rv.headers.add_header('Content-Disposition: attachment', 'filename=' + u.shortname + c.testname + '.py')
    rv.headers.add('Content-Disposition','attachment', filename=u.shortname + c.testname + '.py')
    rv.mimetype = 'text/plain'
    return rv

# filename is one of 'users', 'holidays', 'assignments'
PATHNAMES = {'users':USERSFILE, 'holidays':HOLIDAYSFILE, 'assignments':ASSIGNMENTSFILE}


@app.route('/admin_files/<filename>')
def admin_files(filename):
    u = User(ADMIN)
    if u.isadminsession() and filename in PATHNAMES:
        data = open(PATHNAMES[filename],'r').read()
        return render_template('editfile.html', filename=filename, data=data)
    else:
        return redirect(url_for('site_main'))
    
@app.route('/admin_filessubmit/<filename>', methods=['POST'])
def admin_filessubmit(filename):
    u = User(ADMIN)
    if u.isadminsession() and filename in PATHNAMES:
        data = request.form['data']
        open(PATHNAMES[filename],'w').write(data)
    return redirect(url_for('site_main'))
        
