import os
import time

import requests

from xyw_class import XYW


os.environ['NO_PROXY'] = 'xyw.hainanu.edu.cn'
net = XYW(r'/Users/xin/Documents/Program/Python/auto-login/src')

while True:
    try:
        requests.get('https://www.baidu.com')
        print('网络已连通')
        break
    except requests.exceptions.SSLError as ssl_error:
        print('网络未认证')
        results = net.connect()
        # region 输出中间结果
        # for result in results:
        #     if isinstance(result, tuple):
        #         for item in result:
        #             print(item)
        #     else:
        #         print(result)
        # endregion
    except requests.exceptions.ConnectionError as connection_error:
        print('网络未连接')
        time.sleep(1)
