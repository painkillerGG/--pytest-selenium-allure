import sqlite3
from common.log import log as logger
from settings import ENV, DBsql
import settings

class MysqlAuto(object):
    def __init__(self):
        """连接到sqlite数据库"""
        self.conn = sqlite3.connect(DBsql.sql_file)
        # 创建一个Cursor对象作为属性，用于执行sql命令
        self.cursor = self.conn.cursor()
        logger.info(f'Connected to DB:{DBsql.sql_file}')

    def __del__(self):
        """"对象资源被释放时触发，在对象即将被删除时的最后操作"""
        # 关闭游标和链接
        self.cursor.close()
        self.conn.close()
        logger.info(f'Closed DB:{DBsql.sql_file}')

    def execute(self, sql_list):
        """执行sql语句"""
        try:
            datas=[]
            for i in sql_list:  # 语句列表
                logger.info(f'执行sql: {i}')
                self.cursor.execute(i)
                list1 = self.cursor.fetchall()
                logger.info(f'sql执行结果:{list1}')
                datas.append(list1)
            # 提交事务：
            self.conn.commit()
            logger.debug(datas)
            return datas
        except Exception as e:
            logger.error(f'执行sql出现错误，异常为{e}')
            raise e


if __name__ == '__main__':
    """
     df_cart_cartinfo
     df_goods_goodsinfo
     df_goods_typeinfo
     df_order.orderdetailinfo
     df_order_orderinfo
     df_user_goodsbrowser
     df_user_userinfo
     # 清空
   
     """
    sql =['select *from df_user_userinfo','select * from df_cart_cartinfo']

    # del_sql = 'DELETE FROM df_order_orderinfo;'
    # MysqlAuto().execute(DBSql.sql_list)
    # sql :['select * from df_cart_cartinfo']
    # order id  MysqlAuto().execute(sql)
    # log.info(order_id)
    # log.info(len(order_id))
    # MysqlAuto().execute(settings.DBsql.sql_list)

    MysqlAuto().execute(sql)
