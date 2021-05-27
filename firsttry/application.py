# -*- coding: UTF-8 -*-
import sys
import time
from webob import Request, Response
import json
#from oslo_log import log as logging
#from oslo_config import cfg
#LOG = logging.getLogger(__name__)


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


class SaveApplication(object):
    def __init__(self, in_arg):
        self.in_arg = in_arg

    def __call__(self, environ, start_response):
        req = Request(environ)
        data = json.loads(req.body)
        #LOG.info(u"this is {}".format(json.dumps(data)))
        self.save_to_local(data)
        res = Response()
        res.status = 200
        res.body = "ok"
        return res(environ, start_response)

    def save_to_local(self, data):
        file_path = '{}\\data.txt'.format(sys.path[0])
        with open(file_path, 'a+') as p:
            tmp = u'[{key}] {value}\n'
            for item in data.items():
                wr_str = tmp.format(key=item[0], value=item[1]).encode('utf8')
                p.write(wr_str)
            p.write('\n')


def hi_factory(global_config, in_arg):
    return HelloApplication(in_arg)


def save_factory(global_config, in_arg):
    return SaveApplication(in_arg)
