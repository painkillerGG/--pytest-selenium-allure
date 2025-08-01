import requests
r = requests.get('https://www.baidu.com')
print(r.text)# 通过文本的形式获取响应内容
