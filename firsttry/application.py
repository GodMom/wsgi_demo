# -*- coding: UTF-8 -*-

import time
from webob import Request, Response


class HelloApplication(object):

    def __init__(self, in_arg):
        self.suc_res = "ok,got it, {},time is {}"
        self.false_res = "please input name ovo"
        self.in_arg = in_arg

    def __call__(self, environ, start_response):
        req = Request(environ)
        name = ''
        res = Response()
        try:
            name = req.GET['name']
        except KeyError:
            res.status = 500
            res.body = self.false_res
            return res(environ, start_response)
        if name:
            res.status = 200
            time_now = time.asctime(time.localtime(time.time()))
            res.body = self.suc_res.format(req.GET['name'], time_now).encode('utf8')
            return res(environ, start_response)
        else:
            res.status = 500
            res.body = self.false_res
            return res(environ, start_response)


def hi_factory(global_config, in_arg):
    return HelloApplication(in_arg)

