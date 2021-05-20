# -*- coding: UTF-8 -*-


from wsgiref.simple_server import make_server
import time
from webob import Request, Response


class Application(object):

    def __init__(self):
        self.res = "ok,got it, {},time is {}"

    def __call__(self, environ, start_response):
        req = Request(environ)
        res = Response()
        res.status = 200
        time_now = time.asctime(time.localtime(time.time()))
        res.body = self.res.format(req.GET['name'], time_now).encode('utf8')
        return res(environ, start_response)


app = Application()
server = make_server('172.22.208.81', 64570, app)
server.serve_forever()
