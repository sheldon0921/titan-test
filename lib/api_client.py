import requests
import logging
import allure
import urllib3
import json
from config.settings import config

# 禁用安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.timeout = config.get("timeout", 10)

    def send_request(self, method, url, **kwargs):
        """
        统一请求发送方法
        """
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("verify", False)

        # 日志美化: 尝试将 json 参数转为字符串
        log_data = kwargs.get("json", kwargs.get("data", {}))

        with allure.step(f"🚀 API请求: {method.upper()} {url}"):
            logging.info(f"-------------------------------------------------------")
            logging.info(f"🚀 Request: {method.upper()} {url}")
            logging.info(f"💾 Headers: {kwargs.get('headers', self.session.headers)}")
            logging.info(f"📦 Data: {log_data}")

            # Allure 附件: 请求详情
            allure.attach(str(log_data), name="Request Body", attachment_type=allure.attachment_type.TEXT)

            try:
                response = self.session.request(method, url, **kwargs)

                # 尝试解析 JSON 以便美化打印
                try:
                    resp_json = response.json()
                    log_resp = json.dumps(resp_json, ensure_ascii=False, indent=2)
                except:
                    log_resp = response.text[:1000]  # 非 JSON 或太长，只取前1000字符

                logging.info(f"✅ Response Status: {response.status_code} | Time: {response.elapsed.total_seconds()}s")
                logging.info(f"📄 Response Data: \n{log_resp}")
                logging.info(f"-------------------------------------------------------")

                # Allure 附件: 响应详情
                allure.attach(str(response.status_code), name="Status Code",
                              attachment_type=allure.attachment_type.TEXT)
                allure.attach(log_resp, name="Response Body", attachment_type=allure.attachment_type.TEXT)

                return response

            except Exception as e:
                logging.error(f"❌ 请求异常: {e}")
                allure.attach(str(e), name="Exception", attachment_type=allure.attachment_type.TEXT)
                raise e

    def get(self, url, **kwargs):
        return self.send_request("get", url, **kwargs)

    def post(self, url, **kwargs):
        return self.send_request("post", url, **kwargs)