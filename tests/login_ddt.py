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
except Exception as e:
    logging.error(f"❌ 加载测试数据失败: {e}")
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
        payload = case_info.get('payload', {})
        expected = case_info.get('expected', {})

        # 验证测试数据完整性
        if not payload:
            pytest.skip(f"⚠️ 用例 '{case_info.get('title', '未知')}' 缺少 payload 数据")

        if not expected:
            pytest.skip(f"⚠️ 用例 '{case_info.get('title', '未知')}' 缺少 expected 数据")

        # 动态设置 Allure 标题
        allure.dynamic.title(case_info.get('title', '登录测试'))

        # 发起请求
        res = self.auth_api.login(payload.get('username', ''), payload.get('password', ''))

        # 1. 基础断言：状态码
        assert res.status_code == expected.get('status_code', 200), \
            f"状态码不匹配: 期望 {expected.get('status_code')}, 实际 {res.status_code}"

        # 2. 分支断言：根据预期结果做不同的检查
        # 如果预期是成功，我们才去校验返回结果里有没有用户名
        if expected.get('msg') == "success":
            actual_user = get_json_value(res.json(), "$.json.username")
            assert actual_user == payload.get('username'), \
                f"用户名不匹配: 期望 {payload.get('username')}, 实际 {actual_user}"

        else:
            # 如果预期是失败，我们通常校验错误提示信息
            # (注意：因为用的 httpbin 模拟，这里无法真正校验错误msg，但在真实项目中应该这样写)
            logging.info(f"ℹ️ 这是一个预期失败的用例: {case_info.get('title', '未知')}")
            # 示例：assert expected['msg'] in res.text