# -*- coding: UTF-8 -*-
import sys
import time

import requests

IP = 'localhost'


def create_request(opr):
    print opr
    if opr == "hello":
        with open('user.txt', 'r') as t:
            for i in t.readlines():
                i = i.strip()
                data = {'name': i}
                r = requests.get("http://{}:233/hello".format(IP), params=data)
                print r.text
                time.sleep(1)
    elif opr == "save":
        params = {"title": u"晚上好", 'content': u"test1", 'description': u"none"}
        r = requests.post("http://{}:233/save".format(IP), json=params)
        print r.text


if __name__ == '__main__':
    opr = sys.argv[1]
    create_request(opr)
