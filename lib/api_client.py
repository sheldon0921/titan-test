import requests
import logging
import allure
import urllib3
from typing import Optional, Dict, Any
from config.settings import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.timeout = config.get("timeout", 10)

    def send_request(self, method: str, url: str, **kwargs) -> requests.Response:
        # ... (保持原本的 send_request 逻辑不变) ...
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("verify", False)

        with allure.step(f"🚀 API请求: {method.upper()} {url}"):
            logging.info(f"🚀 发送请求 >>> {method.upper()} {url}")
            try:
                response = self.session.request(method, url, **kwargs)
                log_msg = f"✅ 响应状态: {response.status_code} | 耗时: {response.elapsed.total_seconds()}s"
                if response.status_code >= 400:
                    logging.error(log_msg)
                    allure.attach(response.text[:2000], name="错误响应", attachment_type=allure.attachment_type.TEXT)
                else:
                    logging.info(log_msg)
                return response
            except Exception as e:
                logging.error(f"❌ 请求异常: {e}")
                allure.attach(str(e), name="异常堆栈", attachment_type=allure.attachment_type.TEXT)
                raise e

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.send_request("get", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self.send_request("post", url, **kwargs)
# 👇 新增：手动关闭方法
    def close(self):
        if self.session:
            self.session.close()
            logging.info("🔌 API Session 已关闭")

    # 👇 新增：支持 with 上下文语法
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()