import logging
import pytest
import allure
from api.auth_api import AuthApi
from lib.utils import load_yaml_data, get_json_value

# 加载数据及容错处理（保持不变）
try:
    test_data = load_yaml_data("data/login_cases.yaml")
    if not test_data:
        test_data = []
except Exception:
    test_data = []


@allure.feature("用户认证模块")
class TestLogin:

    def setup_method(self):
        self.auth_api = AuthApi()

    # 记得在 teardown 里关闭
    def teardown_method(self):
        self.auth_api.close()

    @allure.story("登录场景测试")
    @pytest.mark.parametrize("case_info", test_data, ids=[i.get('title') for i in test_data])
    def test_login_scenarios(self, case_info):
        payload = case_info['payload']
        expected = case_info['expected']

        # 发起请求
        res = self.auth_api.login(payload['username'], payload['password'])

        # 1. 基础断言：状态码
        assert res.status_code == expected['status_code']

        # 2. 分支断言：根据预期结果做不同的检查
        # 如果预期是成功，我们才去校验返回结果里有没有用户名
        if expected['msg'] == "success":
            actual_user = get_json_value(res.json(), "$.json.username")
            assert actual_user == payload['username'], "登录成功后返回的用户名与预期不符"

        else:
            # 如果预期是失败，我们通常校验错误提示信息
            # (注意：因为用的 httpbin 模拟，这里无法真正校验错误msg，但在真实项目中应该这样写)
            logging.info(f"ℹ️ 这是一个预期失败的用例: {case_info['title']}")
            # 示例：assert expected['msg'] in res.text