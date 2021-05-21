# -*- coding: UTF-8 -*-
import os
import sys
from wsgiref.simple_server import make_server
import routes as route
from paste.deploy import loadapp

if __name__ == '__main__':
    config = 'configure.ini'
    app_name = 'main'
    wsgi_app = loadapp('config:{}\\{}'.format(sys.path[0], config), app_name)
    server = make_server('localhost', 233, wsgi_app)
    server.serve_forever()
