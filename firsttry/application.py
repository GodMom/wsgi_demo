# -*- coding: UTF-8 -*-
import sys
import os
import time
from webob import Request, Response
import json
import MySQLdb
from jinja2 import Environment, PackageLoader

# from oslo_log import log as logging
# from oslo_config import cfg
# LOG = logging.getLogger(__name__)

DATA_ROUTE = '/root/data.txt'


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
        res = Response()
        if req.body != "":
            data = json.loads(req.body)
            result = self.save_to_db(data)
            self.save_to_local(data)
            res.body = result
        else:
            # LOG.info(u"this is {}".format(json.dumps(data)))
            with open("/root/wsgi_demo/wsgi_demo/firsttry/templates/save.html", 'r') as f:
                data = f.read().decode("utf8")
                res.body = data.encode("utf8")
        res.status = 200
        return res(environ, start_response)

    # 存到本地文件
    def save_to_local(self, data):
        file_path = '{}'.format(DATA_ROUTE)
        with open(file_path, 'a+') as p:
            tmp = u'[{key}] {value}\n'
            for item in data.items():
                wr_str = tmp.format(key=item[0], value=item[1]).encode('utf8')
                p.write(wr_str)
            p.write('\n')

    # 存入数据库
    def save_to_db(self, data):
        db = MySQLdb.connect("localhost", "root", "Xy269420+", "deep", charset="utf8")
        cursor = db.cursor()
        result = ''
        sql = u"INSERT INTO beiwang(title, content, description) VALUES ('%s', '%s', '%s')" % \
              (data.get('title', u"无"), data.get('content', u"无"), data.get('description', u""))
        sql = sql.encode("utf8")
        try:
            cursor.execute(sql)
            db.commit()
            result = u"ok"
        except Exception as e:
            db.rollback()
            result = u"insert failed!"
        db.close()
        return result.encode("utf8")


class ListApplication(object):
    def __init__(self, in_arg):
        self.in_arg = in_arg

    def __call__(self, environ, start_response):
        req = Request(environ)
        res = Response()
        content = u""
        data = self.select_from_db()
        content += data
        res.status = 200
        res.body = content.encode('utf8')
        return res(environ, start_response)

    def select_from_db(self):
        def make_template(datas):
            env = Environment(loader=PackageLoader("/root/wsgi_demo/wsgi_demo/firsttry/", "templates"))
            template = env.get_template("list.html")
            result = template.render(list(datas))
            print result
            return result

        db = MySQLdb.connect("localhost", "root", "Xy269420+", "deep", charset="utf8")
        cursor = db.cursor()
        sql = u"select * from beiwang"
        cursor.execute(sql)
        res = cursor.fetchall()
        data = make_template(res)
        return data


def hi_factory(global_config, in_arg):
    return HelloApplication(in_arg)


def save_factory(global_config, in_arg):
    return SaveApplication(in_arg)


def list_factory(global_config, in_arg):
    return ListApplication(in_arg)


