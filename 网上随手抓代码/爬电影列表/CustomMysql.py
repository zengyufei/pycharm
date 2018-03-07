import sys
import pymysql


class Mysql:
    host = '127.0.0.1'
    port = 3306
    username = 'root'
    password = 'root'

    def __str__(self):
        return '\n'.join(['%s: %s' % item for item in self.__dict__.items()])

    def __init__(self, host=None, port=None, username=None, password=None, db=None, charset=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db = db
        self.charset = charset
        if charset == None:
            charset = 'utf8'
        # 创建连接
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.username, passwd=self.password, db=db,
                                    charset=charset)
        # 创建游标
        self.cursor = self.conn.cursor()

    def getConn(self):
        return self.conn

    def getCursor(self):
        return self.cursor

    def execute(self, sql):
        try:
            #  执行 sql 语句
            self.cursor.execute(sql)
            #  提交到数据库执行
            self.conn.commit()
        except:
            #  如果发生错误则回滚
            self.conn.rollback()
            print("执行语句错误，且回滚了 = ", sql)
        return self.cursor

    def count(self, sql):
        try:
            row = self.cursor.execute(sql)
            if row > 0:
                return self.cursor.fetchone()[0]
            else:
                return 0
        except:
            print("统计语句错误 = ", sql)

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
            print("新增语句错误，且回滚了 = ", sql, "。 异常为：",  sys.exc_info())

    def insertAll(self, sql):
        try:
            # cursor.executemany("insert into tb7(user,pass,licnese)values(%s,%s,%s)", [("u1","u1pass","11111"),("u2","u2pass","22222")])
            self.cursor.executemany(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
            print("批量新增语句错误，且回滚了 = ", sql)

    def get(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except:
            return "查询语句错误 = ", sql

    def list(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            return "查询语句错误 = ", sql

    def close(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()
