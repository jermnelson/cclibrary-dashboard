#!/home/CCLibrary/python-env/bin/python

from flup.server.fcgi import WSGIServer
from app import dashboard

if __name__ == '__main__':
    WSGIServer(dashboard,
               bindAddress=('0.0.0.0', 10001)).run()
