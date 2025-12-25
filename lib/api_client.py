# lib/api_client.py
import requests
import logging
import allure  # 导入 allure


class ApiClient:
    def __init__(self):
        self.session = requests.Session()

    def send_request(self, method, url, **kwargs):
        # 使用 allure.step 将这个动作显示在报告的步骤条里
        # title 里的 {} 会被自动替换成变量值
        with allure.step(f"🚀 API请求: {method.upper()} {url}"):

            logging.info(f"🚀 发送请求 >>> {method.upper()} {url}")

            # 如果有请求体，把它附加到报告详情里
            if "json" in kwargs:
                allure.attach(str(kwargs['json']), name="请求参数", attachment_type=allure.attachment_type.TEXT)

            try:
                response = self.session.request(method, url, **kwargs)

                logging.info(f"✅ 响应状态: {response.status_code}")

                # 把响应结果也附加到报告里
                allure.attach(str(response.status_code), name="响应状态码", attachment_type=allure.attachment_type.TEXT)
                allure.attach(response.text[:500], name="响应内容(前500字符)",
                              attachment_type=allure.attachment_type.TEXT)

                return response

            except Exception as e:
                logging.error(f"❌ 请求炸了: {e}")
                allure.attach(str(e), name="异常信息", attachment_type=allure.attachment_type.TEXT)
                raise e