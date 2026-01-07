import pymysql
import logging
from config.settings import config


class DBUtils:
    """
    数据库操作工具类 (支持上下文管理器)
    使用方式:
    with DBUtils() as db:
        res = db.query_one("SELECT * FROM users")
    """

    def __init__(self):
        # 读取配置，增加默认值防止报错
        db_conf = config.get('db', {})
        self.host = db_conf.get('host', '127.0.0.1')
        self.port = db_conf.get('port', 3306)
        self.user = db_conf.get('user', 'root')
        self.password = db_conf.get('password', '')
        self.db_name = db_conf.get('name', 'test_db')
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        进入 with 语句时触发：建立连接
        """
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor  # 👈 优化：返回字典格式，方便取值
            )
            self.cursor = self.conn.cursor()
            logging.debug("🔌 数据库连接已建立")
            return self
        except Exception as e:
            logging.error(f"❌ 数据库连接失败: {e}")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出 with 语句时触发：关闭资源
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logging.debug("🔌 数据库连接已关闭")

    def query_one(self, sql):
        """查询单条记录"""
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except Exception as e:
            logging.error(f"❌ SQL执行报错: {sql} | Error: {e}")
            return None

    def query_all(self, sql):
        """查询多条记录"""
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"❌ SQL执行报错: {sql} | Error: {e}")
            return None

    def execute(self, sql):
        """执行增删改操作 (自动提交)"""
        try:
            rows = self.cursor.execute(sql)
            self.conn.commit()
            return rows
        except Exception as e:
            self.conn.rollback()
            logging.error(f"❌ SQL执行失败，已回滚: {sql} | Error: {e}")
            return 0