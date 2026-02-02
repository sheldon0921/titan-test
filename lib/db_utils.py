from typing import Optional, Dict, Any, List, Union
import pymysql
import logging
from contextlib import contextmanager
from config.settings import config

class DBUtils:
    def __init__(self) -> None:
        # 1. 修复配置读取 Bug：从 'db' 字典中获取
        db_conf = config.get('db', {})
        self.host: Optional[str] = db_conf.get('host')
        self.user: Optional[str] = db_conf.get('user')
        self.password: Optional[str] = db_conf.get('password')
        self.db_name: Optional[str] = db_conf.get('name')
        self.port: int = db_conf.get('port', 3306)
        self.conn: Optional[pymysql.connections.Connection] = None
        self.cursor: Optional[pymysql.cursors.DictCursor] = None

    def connect(self):
        """建立数据库连接"""
        if not all([self.host, self.user, self.db_name]):
            raise ValueError("数据库配置不完整，缺少必要的连接参数")

        try:
            if self.conn is None or not self.conn.open:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password or "",
                    database=self.db_name,
                    port=self.port,
                    charset='utf8mb4',
                    # 2. 优化：使用字典游标，查询结果返回 {'id': 1} 而不是 (1,)
                    cursorclass=pymysql.cursors.DictCursor
                )
            return self.conn
        except pymysql.Error as e:
            logging.error(f"❌ 数据库连接失败: {e}")
            raise ConnectionError(f"数据库连接失败: {self.host}:{self.port}/{self.db_name} - {e}") from e
        except Exception as e:
            logging.error(f"❌ 数据库连接异常: {e}")
            raise RuntimeError(f"数据库连接异常: {e}") from e

    def query_one(self, sql: str) -> Optional[Dict[str, Any]]:
        """查询单条记录
        :param sql: SQL 查询语句
        :return: 单条记录字典，如果未找到返回 None
        """
        if not sql or not isinstance(sql, str):
            raise ValueError("SQL 语句必须是非空字符串")

        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()
        except pymysql.Error as e:
            logging.error(f"❌ SQL执行异常: {sql} | 错误: {e}")
            raise RuntimeError(f"SQL 执行失败: {e}") from e
        except Exception as e:
            logging.error(f"❌ SQL执行异常: {sql} | 错误: {e}")
            raise RuntimeError(f"SQL 执行异常: {e}") from e
            # 注意：这里我们不关闭连接，配合 setup/teardown 模式复用连接

    def query_all(self, sql: str) -> List[Dict[str, Any]]:
        """查询多条记录
        :param sql: SQL 查询语句
        :return: 记录列表
        """
        if not sql or not isinstance(sql, str):
            raise ValueError("SQL 语句必须是非空字符串")

        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except pymysql.Error as e:
            logging.error(f"❌ SQL执行异常: {sql} | 错误: {e}")
            raise RuntimeError(f"SQL 执行失败: {e}") from e
        except Exception as e:
            logging.error(f"❌ SQL执行异常: {sql} | 错误: {e}")
            raise RuntimeError(f"SQL 执行异常: {e}") from e

    def execute(self, sql: str, params: Optional[Union[tuple, Dict[str, Any]]] = None) -> int:
        """执行增删改操作
        :param sql: SQL 语句
        :param params: 参数元组或字典
        :return: 影响的行数
        """
        if not sql or not isinstance(sql, str):
            raise ValueError("SQL 语句必须是非空字符串")

        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, params)
                conn.commit()
                logging.info(f"✅ SQL执行成功，影响行数: {affected_rows}")
                return affected_rows
        except pymysql.Error as e:
            conn.rollback()
            logging.error(f"❌ SQL执行异常: {sql} | 错误: {e}")
            raise RuntimeError(f"SQL 执行失败: {e}") from e
        except Exception as e:
            conn.rollback()
            logging.error(f"❌ SQL执行异常: {sql} | 错误: {e}")
            raise RuntimeError(f"SQL 执行异常: {e}") from e

    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
        conn = self.connect()
        try:
            yield conn
            conn.commit()
            logging.info("✅ 事务提交成功")
        except Exception as e:
            conn.rollback()
            logging.error(f"❌ 事务回滚: {e}")
            raise RuntimeError(f"事务失败: {e}") from e

    def close(self) -> None:
        """关闭连接"""
        if self.conn and self.conn.open:
            self.conn.close()
            logging.info("🛢️ 数据库连接已关闭")

    # 3. 新增：支持上下文管理器写法 (with DBUtils() as db:)
    def __enter__(self) -> 'DBUtils':
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()