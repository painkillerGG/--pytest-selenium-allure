import requests

from settings import ENV

#百度翻译
# url='https://ts1.tc.mm.bing.net/th/id/OIP-C.KnOS3vOcNhLla8LSZw4TugHaHa?w=144&h=144&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2'
# headers={'User-Agent':'Mozilla/4.0'}
# html=requests.get(url,headers=headers).content
# with open(r'D:\python program\study\PythonProject\auto-ui-minjianPC\draft\python_logo.jpg','wb') as f:
#     f.write(html)
Cookie="Admin-Token=7627e43948995cca9c5c930ed20586b8e6e03d2bc5b43935ac6225f28674e4f21dd83fbd3e7e62dcdec2e0d9c93a12f38aeabe2bcd920cc4126f3587ba6b131b45149e40f5b548158e5964805d4129d4e7e36186e9dea7ec; UserInfo={%22id%22:46%2C%22roleId%22:1%2C%22roleName%22:%22%E8%B6%85%E7%BA%A7%E7%AE%A1%E7%90%86%E5%91%98%22%2C%22userId%22:103%2C%22avatar%22:%22http://192.168.31.88:9000/xqhztest-public/static/user/avatar/img/20250529/8820e1c7-49fd-4f02-a1cc-c7c65045f12a.png%22%2C%22email%22:%22454656546546545646546545@qq.com%22%2C%22phone%22:%2213110298364%22%2C%22username%22:%22lbw%22%2C%22adminRoleType%22:%22SYSTEM%22%2C%22menuInfos%22:[]}"
url=f'{ENV.APIURL}/api/admin/policy/article/page'
headers = {
    'version':'1.0.0',
    'ADMIN-phone':'13110298364',
    'ADMIN-userID':'113',
    'ADMIN-username':'lbw',
    'Cookie':Cookie,
}
data={
    'page':'1',
    'size':'10',
    'status':'PUSH'
}
response=requests.get(url,headers=headers,params=data)
print(response.json())