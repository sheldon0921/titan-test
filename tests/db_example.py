import pytest
import allure
import logging
from lib.db_utils import DBUtils


@allure.feature("数据一致性检查")
class TestDBVerification:

    def setup_method(self):
        # ⚠️ 注意：由于没有真实的数据库环境，这里实例化可能会失败
        # 在实际项目中，这里会连接 config/env.yaml 里配置的数据库
        try:
            self.db = DBUtils()
        except Exception as e:
            logging.warning(f"数据库连接失败 (预期内，如果是本地无环境): {e}")
            self.db = None

    def teardown_method(self):
        if self.db:
            self.db.close()

    @allure.story("验证用户注册数据落库")
    @pytest.mark.skipif(True, reason="没有真实数据库环境，暂时跳过")
    def test_user_creation_in_db(self):
        """
        演示：调用注册接口后，查库验证数据
        """
        username = "new_user_001"

        # 1. 假设这里调用了注册接口
        # api.register(username, ...)
        logging.info(f"模拟注册用户: {username}")

        # 2. 数据库断言
        if self.db:
            sql = f"SELECT count(*) FROM users WHERE username = '{username}'"
            result = self.db.query_one(sql)

            # 断言查到了 1 条记录
            assert result[0] == 1
            logging.info("✅ 数据库验证通过")