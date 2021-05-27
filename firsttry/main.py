# -*- coding: UTF-8 -*-
import os
import sys
import eventlet
from eventlet import wsgi
from wsgiref.simple_server import make_server
import routes as route
from paste.deploy import loadapp

IP = 'localhost'


if __name__ == '__main__':
    config = 'configure.ini'
    app_name = 'main'
    wsgi_app = loadapp('config:{}\\{}'.format(sys.path[0], config), app_name)
    try:
        server = eventlet.spawn(wsgi.server,
                                eventlet.listen((IP, 233)), wsgi_app)
    except Exception:
        raise
    print "ok,server runs on ip {IP} port {port}".format(IP=IP, port=233)
    server.wait()
