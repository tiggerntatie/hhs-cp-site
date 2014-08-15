import sys, os

path = '/home/www/htdocs/hhscp.org/wsgi'
if path not in sys.path:
    sys.path.append(path)

os.chdir('/home/www/htdocs/hhscp.org/wsgi')

from hhscp import app as application
