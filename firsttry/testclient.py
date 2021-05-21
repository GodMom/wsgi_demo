# -*- coding: UTF-8 -*-
import time

import requests

with open('user.txt', 'r') as t:
    for i in t.readlines():
        i = i.strip()
        data = {'name': i}
        r = requests.get("http://localhost:233/hello", params=data)
        print r.text
        time.sleep(1)


