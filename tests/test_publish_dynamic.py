import pytest
import allure
import logging


@allure.feature("社区动态模块")
class TestPublishDynamic:

    @allure.story("发布动态")
    @allure.description("发布动态接口测试")
    def test_publish_dynamic_custom_headers(self, auth_client):
        """
        :param auth_client: 已包含公共 Headers (User-Agent, Content-Type 等)
        """
        url = f"{auth_client.base_url}/circle/dynamic/publishdynamic"

        payload = {
            "content": "“桃園三結義，江南無所有，聊贈一枝春。”萌寵相伴，春意滿懷，紙短情長，歲月溫柔。 🚀",
            "check_status":	1,
            "dynamic_id": 0,
            "files_ids":"696589"
        }


        # ----------------------------------------
        # 场景：该接口需要额外的渠道标识，或者需要覆盖默认的 User-Agent
        custom_headers = {
            "api-client": "iOS",
            "sign": "d9ac3282e89f64ad33ffc6fb6eddccf7",
            "timestamp": "1768878451199",
            "platform":"app"
        }

        logging.info(f"📤 发送请求，附带个性化 Headers: {custom_headers}")

        # 直接将 headers 参数传给 post 方法
        # 底层逻辑：requests 会自动做 merge 操作
        res = auth_client.post(url, json=payload, headers=custom_headers)
        logging.info(res.json())

        assert res.status_code == 200


        logging.info("✅ 接口调用成功，个性化 Headers 已生效")








