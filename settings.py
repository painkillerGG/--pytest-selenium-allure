class ENV:
    # 被测环境

    URL = 'http://192.168.31.201/dataCenters/userAnalyse'
    # 自动化专用账号
    username = '15000000001'
    password = 'xqpt88888888'
    phoneverifycode = '1234'
    test_txt = r"D:\python program\study\PythonProject\auto-ui-minjianPC\source\test.txt"
    picture = r"D:\python program\study\PythonProject\auto-ui-minjianPC\source\test.png"

    # 接口信息
    APIURL = "http://192.168.31.111:7086"
    headers = {'version': '1.0.0',
               'ADMIN-phone': '15000000001',
               'ADMIN-userID': '198',
               'ADMIN-username': 'auto-ui',
               'Cookie':"Admin-Token=9943e76f3804e1b7566269631509f7728f7d24405a260368ac4bdf22cdb35829cf20e45ed8265cbe27d971ecafcc4f1e161f83b11e0c88be432fccfbfa970d92fa9d27eb71b08de48f405aef142d17f0d3f2273b1a6899f685fa0364784fa8e3; UserInfo={%22id%22:83%2C%22roleId%22:1%2C%22roleName%22:%22%E8%B6%85%E7%BA%A7%E7%AE%A1%E7%90%86%E5%91%98%22%2C%22userId%22:198%2C%22avatar%22:null%2C%22email%22:null%2C%22phone%22:%2215000000001%22%2C%22username%22:%22auto-ui%22%2C%22adminRoleType%22:%22SYSTEM%22%2C%22menuInfos%22:[]}"
                        ,
               'Token': "46a4446740e6df39cd2d54e17cd181732eca98d0b2c222da17c89d8d9563a5d007d5f3583b572eb50c1805487bf9e989b6d959e1bb7a934301f6826c3e83cb6e160b48edac185f4432cba623f2206e1cf95a1489e7443f948031c0624cbe0f5e"
               ,'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'
               }


class DBsql:
    """初始化时清除数据sql语句
    清空：用户、购物车、订单信息
    并插入：测试用户test123456"""
    sql_file = rf'D:\python program\project\daily_fresh_demo-master\daily_fresh_demo-master\db.sqlite3'
    sql_list = [
        'DELETE FROM df_order_orderdetailinfo',
        'DELETE FROM df_order_orderinfo',
        'DELETE FROM df_user_userinfo',
        'DELETE FROM df_cart_cartinfo',
        "INSERT INTO 'df_user_userinfo' VALUES ('41','painkiller','692834f0179a1aa9b6114c5bf7583cb9c7fce322',"
        "'38440494@qq.com','','','','')"

    ]
