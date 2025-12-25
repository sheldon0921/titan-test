# tests/test_login_ddt.py
import pytest
import logging
from lib.api_client import ApiClient
from lib.utils import load_yaml_data
from config.settings import config

# 1. 加载数据 (装弹)
test_data = load_yaml_data("data/login_cases.yaml")


class TestLogin:

    # 2. 参数化装饰器 (瞄准)
    # ids 用来在测试报告里给每个用例起名字，方便区分
    @pytest.mark.parametrize("case_info", test_data, ids=[item['title'] for item in test_data])
    def test_login_scenarios(self, case_info):
        """
        这个函数会运行 3 次！每次 case_info 的值都不一样。
        """
        logging.info(f"▶️ 开始执行测试用例: {case_info['title']}")

        # 准备数据
        url = f"{config['base_url'].rstrip('/')}/post"
        payload = case_info['payload']
        expected = case_info['expected']

        # 发送请求
        client = ApiClient()
        res = client.send_request("post", url, json=payload)

        # 验证结果 (这里我们验证 httpbin 是否正确接收了我们的参数)
        assert res.status_code == expected['status_code']

        # 模拟业务断言：验证我们要发的数据真的发出去了
        # (真实项目中，这里通常是 assert res.json()['code'] == expected['code'])
        assert res.json()['json']['username'] == payload['username']

        logging.info("✅ 用例通过！")