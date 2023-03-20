import os

import requests

from xyw_class import XYW


os.environ['NO_PROXY'] = 'xyw.hainanu.edu.cn'

try:
    requests.get('https://www.baidu.com')
except requests.exceptions.RequestException:
    print('网络未认证')
    net = XYW(r'/Users/xin/Program/Python/auto-login/src')
    try:
        net.connect()
    except requests.exceptions.RequestException:
        print('网络认证失败')

print('网络已连通')
