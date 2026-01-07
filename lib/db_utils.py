import pymysql
import logging
from config.settings import config

class DBUtils:
    def __init__(self):
        # 1. 修复配置读取 Bug：从 'db' 字典中获取
        db_conf = config.get('db', {})
        self.host = db_conf.get('host')
        self.user = db_conf.get('user')
        self.password = db_conf.get('password')
        self.db_name = db_conf.get('name')
        self.port = db_conf.get('port', 3306)
        self.conn = None

    def connect(self):
        """建立数据库连接"""
        try:
            if self.conn is None or not self.conn.open:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.db_name,
                    port=self.port,
                    charset='utf8mb4',
                    # 2. 优化：使用字典游标，查询结果返回 {'id': 1} 而不是 (1,)
                    cursorclass=pymysql.cursors.DictCursor
                )
            return self.conn
        except Exception as e:
            logging.error(f"❌ 数据库连接失败: {e}")
            raise e

    def query_one(self, sql):
        """查询单条记录"""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()
        except Exception as e:
            logging.error(f"❌ SQL执行异常: {sql} | 错误: {e}")
            raise e
            # 注意：这里我们不关闭连接，配合 setup/teardown 模式复用连接

    def close(self):
        """关闭连接"""
        if self.conn and self.conn.open:
            self.conn.close()
            logging.info("🛢️ 数据库连接已关闭")

    # 3. 新增：支持上下文管理器写法 (with DBUtils() as db:)
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()