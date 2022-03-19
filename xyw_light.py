import base64
import json
import os
import re
from urllib import parse

import requests

# 接口地址
index_url = 'https://xyw.hainanu.edu.cn/srun_portal_pc?ac_id=1&theme=pro'
token_url = 'https://xyw.hainanu.edu.cn/cgi-bin/get_challenge?'
login_url = 'https://xyw.hainanu.edu.cn/cgi-bin/srun_portal?'

# 指定工作目录，方便集成脚本到其他工具（如 utools）
workspace = r'D:\TASK\Program\Python\project\demo\src\xywlogin'
os.chdir(workspace)
with open('config.json') as config_file:
    config = json.load(config_file)

# 该参数必须要，但是内容不重要
callback_str = 'jQuery1124'

# 获取 ip并更新配置
config.update({'ip': re.search(r'ip\s*: "(.*?)",', requests.get(index_url).text).group(1)})

# token请求参数
token_params = {
    'callback': callback_str,
    'username': config['username'],
    'ip': config['ip'],
}

# 获取token并更新配置
token_res = requests.get(token_url + parse.urlencode(token_params))
config.update({'token': re.search(r'"challenge":"(.*?)",', token_res.text).group(1)})

# 切换至js文件目录
os.chdir(os.path.join(os.getcwd(), 'js'))

# 计算 hmd5 和 info 并更新
config.update({
    'hmd5': os.popen(f'node pwd.js {base64.b64encode(json.dumps(config).encode()).decode()}').read().strip(),
    "i": os.popen(f'node info.js {base64.b64encode(json.dumps(config).encode()).decode()}').read().strip()
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
}

login_res = requests.get(login_url + parse.urlencode(login_params))
# print(login_res.text)
