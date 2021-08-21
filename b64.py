
# base64编码和解码

# md5固定长度, 不可反解
# base64变长, 可反解

import base64
import json
dic = {'name':'pzyo', 'age':23, 'sex':'男'}
dic_str = json.dumps(dic)
print(type(dic_str))  # <class 'str'>

# 编码与解码的处理对象是byte, 故对原数据要先编码, 使原本的str类型变成byte
ret = base64.b64encode(dic_str.encode())
print(ret)  # b'eyJuYW1lIjogInB6eW8iLCAiYWdlIjogMjMsICJzZXgiOiAiXHU3NTM3In0='

# 解码
# ret是带解码的串
ret2 = base64.b64decode(ret)
print(type(ret2))  # <class 'bytes'>
print(ret2.decode('utf-8'))  # {"name": "pzyo", "age": 23, "sex": "\u7537"}
print(json.loads(ret2))  # {'name': 'pzyo', 'age': 23, 'sex': '男'}
