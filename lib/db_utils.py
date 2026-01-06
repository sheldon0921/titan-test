import pymysql
from config.settings import config


class DBUtils:
    def __init__(self):
        # 假设您在 env.yaml 里加了 db 配置
        self.host = config.get('db_host')
        self.user = config.get('db_user')
        self.password = config.get('db_password')
        self.db_name = config.get('db_name')
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name,
            charset='utf8mb4'
        )
        return self.conn.cursor()

    def query_one(self, sql):
        """查询单条记录"""
        with self.connect() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()

    def close(self):
        if self.conn:
            self.conn.close()



