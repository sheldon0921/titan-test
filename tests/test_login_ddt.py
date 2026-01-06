import pytest
import allure
from api.auth_api import AuthApi
from lib.utils import load_yaml_data

# 加载数据
test_data = load_yaml_data("data/login_cases.yaml")

@allure.feature("用户认证模块")
class TestLogin:

    def setup_method(self):
        # 每个用例开始前实例化 API 对象
        self.auth_api = AuthApi()

    @allure.story("登录场景测试")
    @pytest.mark.parametrize("case_info", test_data, ids=[i['title'] for i in test_data])
    def test_login_scenarios(self, case_info):
        payload = case_info['payload']
        expected = case_info['expected']

        # 1. 调用业务方法 (代码可读性变强)
        res = self.auth_api.login(payload['username'], payload['password'])

        # 2. 断言
        assert res.status_code == expected['status_code']
        # 建议封装通用的 JSON 断言工具
        assert res.json()['json']['username'] == payload['username']