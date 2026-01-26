import pytest
import allure
import logging
from lib.utils import load_yaml_data

# 1. 加载 YAML 数据
# 注意：为了防止文件不存在导致报错，最好做个容错，或者确保文件路径正确
try:
    test_data = load_yaml_data("data/publish_dynamic_cases.yaml")
    if not test_data:
        logging.warning("⚠️ 数据文件为空或读取失败")
        test_data = []
except Exception as e:
    logging.error(f"❌ 加载测试数据异常: {e}")
    test_data = []


@allure.feature("社区动态模块")
class TestPublishDynamic:

    @allure.story("发布动态")
    @allure.description("发布动态接口测试（数据驱动版）")
    @pytest.mark.parametrize("case_info", test_data, ids=[i.get('title') for i in test_data])
    def test_publish_dynamic(self, case_info, auth_client):
        """
        :param case_info: 从 yaml 中读取的单条测试数据
        :param auth_client: 鉴权 Fixture
        """
        # 2. 从 case_info 中提取数据
        title = case_info.get("title")
        payload = case_info.get("payload")
        headers = case_info.get("headers")  # 可能是 None
        expected = case_info.get("expected")

        # 动态更新 Allure 报告的标题，让报告更清晰
        allure.dynamic.title(title)

        url = f"{auth_client.base_url}/circle/dynamic/publishdynamic"

        logging.info(f"🚀 开始执行用例: {title}")
        logging.info(f"📤 Payload: {payload}")
        if headers:
            logging.info(f"🎩 Custom Headers: {headers}")

        # 3. 发送请求
        # auth_client.post 底层会自动合并 session headers 和这里的 headers
        res = auth_client.post(url, json=payload, headers=headers)

        # 打印响应以便调试
        logging.info(f"📥 Response: {res.text}")

        # 4. 断言
        # 断言状态码
        assert res.status_code == expected.get("status_code", 200)

        # 示例：断言业务逻辑（假设返回结构里有 msg 字段）
        # if "msg" in expected:
        #     assert expected["msg"] in res.text