import os
import re
import time

from xyw_class import XYW

net = XYW(r'D:\TASK\Program\Python\project\demo\src\xywlogin')

while True:
    try:
        net.run()
        ping = os.popen('ping www.baidu.com').read()
        received = re.search(r'已接收 = (\d)', ping).group(1)
        print(received)
        if int(received) != 0:
            print('已连接')
            break
    except Exception as e:
        print(e)
        time.sleep(1)
