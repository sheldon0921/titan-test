import logging

import pytest
import allure
from api.auth_api import AuthApi
from lib.utils import load_yaml_data, get_json_value # 👈 导入新工具

test_data = load_yaml_data("data/login_cases.yaml")
# 1. 增加容错：如果读取失败，给一个默认空列表，防止 Pytest 收集报错
try:
    test_data = load_yaml_data("data/login_cases.yaml")
    if not test_data:
        logging.warning("⚠️ 测试数据为空: data/login_cases.yaml")
        test_data = []
except Exception as e:
    logging.error(f"❌ 加载测试数据失败: {e}")
    test_data = []

@allure.feature("用户认证模块")
class TestLogin:
    def setup_method(self):
        self.auth_api = AuthApi()
    @allure.story("登录场景测试")
    @pytest.mark.parametrize("case_info", test_data, ids=[i['title'] for i in test_data])
    def test_login_scenarios(self, case_info):
        payload = case_info['payload']
        expected = case_info['expected']

        res = self.auth_api.login(payload['username'], payload['password'])

        # 断言状态码
        assert res.status_code == expected['status_code']

        # 🎯 使用 JSONPath 进行灵活断言
        # 假设 httpbin 返回结构很深，用 jsonpath 提取会非常方便
        # 例如验证返回的 json 数据中 username 是否正确
        actual_user = get_json_value(res.json(), "$.json.username")
        assert actual_user == payload['username']
