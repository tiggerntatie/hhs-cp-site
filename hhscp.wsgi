import sys, os

path = '/home/www/htdocs/netdenizen.org/wsgi'
if path not in sys.path:
    sys.path.append(path)

os.chdir('/home/www/htdocs/netdenizen.org/wsgi/hhscp')

from hhscp import app as application
