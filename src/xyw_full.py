import base64
import json
import os
import random
import re
import time
from urllib import parse

import requests

# 请求头
headers = {
    'Host': 'xyw.hainanu.edu.cn',
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://xyw.hainanu.edu.cn/srun_portal_pc?ac_id=1&theme=pro',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'lang=zh-CN'
}

# 接口地址
index_url = 'https://xyw.hainanu.edu.cn/srun_portal_pc?ac_id=1&theme=pro'
status_url = 'https://xyw.hainanu.edu.cn/cgi-bin/rad_user_info?'
token_url = 'https://xyw.hainanu.edu.cn/cgi-bin/get_challenge?'
login_url = 'https://xyw.hainanu.edu.cn/cgi-bin/srun_portal?'

# 指定工作目录，方便集成脚本到其他工具（如 utools）
workspace = r'D:\TASK\Program\Python\project\demo\src\xywlogin'
os.chdir(workspace)
with open('config.json') as config_file:
    config = json.load(config_file)

# 初始化时间戳
cb_time = int(time.time() * 1000)

# 随机callback名称
suffix = str(random.random())
while len(suffix) != 18:
    suffix = str(random.random())
jQuery_cb = 'jQuery1124' + re.sub(r'\D', '', suffix)
callback_str = jQuery_cb + '_' + str(cb_time)

# 获取 ip 并更新配置
ip = re.search(r'ip\s*: "(.*?)",', requests.get(index_url).text).group(1)
config.update({'ip': ip})

# status 请求参数
status_params = {
    'callback': callback_str,
    '_': cb_time + 1
}

# 查询状态
status_res = requests.get(status_url + parse.urlencode(status_params), headers=headers)
# print(status_params)
print(status_res.text)

# token请求参数
token_params = {
    'callback': callback_str,
    'username': config['username'],
    'ip': config['ip'],
    '_': cb_time + 2
}

# 获取 token 并更新配置
token_res = requests.get(token_url + parse.urlencode(token_params), headers=headers)
token = re.search(r'"challenge":"(.*?)",', token_res.text).group(1)
config.update({'token': token})
# print(token)
# print(token_params)
print(token_res.text)

# 切换至js文件目录
os.chdir(os.path.join(os.getcwd(), 'js'))

# 计算 hmd5 和 info 并更新
config_str = base64.b64encode(json.dumps(config).encode()).decode()
config.update({
    'hmd5': os.popen(f'node pwd.js {config_str}').read().strip(),
    "i": os.popen(f'node info.js {config_str}').read().strip()
})

# 计算 checksum 并更新
config.update({
    'checksum': os.popen(f'node checksum.js {base64.b64encode(json.dumps(config).encode()).decode()}').read().strip()
})

# 登录请求参数
login_params = {
    'callback': callback_str,
    'action': 'login',
    'username': config['username'],
    'password': '{MD5}' + config['hmd5'],
    'os': config['os'],
    'name': config['name'],
    'double_stack': config['double_stack'],
    'chksum': config['checksum'],
    'info': config['i'],
    'ac_id': config['acid'],
    'ip': config['ip'],
    'n': config['n'],
    'type': config['type'],
    '_': cb_time + 3
}

final_url = login_url + parse.urlencode(login_params)
login_res = requests.get(final_url, headers=headers)
# print(final_url)
# print(login_params)
print(login_res.text)
