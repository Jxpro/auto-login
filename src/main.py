import os

import requests

from xyw_class import XYW


os.environ['NO_PROXY'] = 'xyw.hainanu.edu.cn'

try:
    requests.get('https://www.baidu.com')
    print('网络已连通')
except requests.exceptions.RequestException:
    print('网络未认证')
    net = XYW(r'/Users/xin/Documents/Program/Python/auto-login/src')
    try:
        net.connect()
        print('网络已连通')
    except requests.exceptions.RequestException:
        print('网络认证失败')
