# -*- coding: UTF-8 -*-
import time

import requests

with open('user.txt', 'r') as t:
    for i in t.readlines():
        i = i.strip()
        if i != '':
            data = {'name': i}
            r = requests.get("http://172.22.208.81:64570", params=data)
            print r.text
            time.sleep(1)


