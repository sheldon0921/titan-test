import requests
import logging
import allure
import urllib3
import json  # 👈 新增导入
from typing import Optional, Dict, Any
from config.settings import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.timeout = config.get("timeout", 10)

    def send_request(self, method: str, url: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("verify", False)

        # 优化：在报告步骤中清晰展示方法和URL
        with allure.step(f"🚀 API请求: {method.upper()} {url}"):
            logging.info(f"🚀 发送请求 >>> {method.upper()} {url}")

            # --- 📌 优化点：将请求参数附加到报告中 ---
            if kwargs.get("json"):
                allure.attach(json.dumps(kwargs["json"], indent=2, ensure_ascii=False),
                              name="请求 Body (JSON)",
                              attachment_type=allure.attachment_type.JSON)
            if kwargs.get("params"):
                allure.attach(json.dumps(kwargs["params"], indent=2, ensure_ascii=False),
                              name="请求 Params",
                              attachment_type=allure.attachment_type.JSON)
            # ----------------------------------------

            try:
                response = self.session.request(method, url, **kwargs)
                log_msg = f"✅ 响应状态: {response.status_code} | 耗时: {response.elapsed.total_seconds()}s"

                # --- 📌 优化点：无论成功失败，都记录响应内容（可视情况截断）---
                # 尝试格式化 JSON 响应以便阅读
                try:
                    resp_text = json.dumps(response.json(), indent=2, ensure_ascii=False)
                    attach_type = allure.attachment_type.JSON
                except:
                    resp_text = response.text
                    attach_type = allure.attachment_type.TEXT

                allure.attach(resp_text, name="响应 Body", attachment_type=attach_type)
                # -----------------------------------------------------------

                if response.status_code >= 400:
                    logging.error(log_msg)
                    # 失败时额外标记
                    allure.attach(str(response.status_code), name="失败状态码",
                                  attachment_type=allure.attachment_type.TEXT)
                else:
                    logging.info(log_msg)

                return response

            except Exception as e:
                logging.error(f"❌ 请求异常: {e}")
                allure.attach(str(e), name="异常堆栈", attachment_type=allure.attachment_type.TEXT)
                raise e

    # ... (其余方法保持不变) ...
    def get(self, url: str, **kwargs) -> requests.Response:
        return self.send_request("get", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self.send_request("post", url, **kwargs)

    def close(self):
        if self.session:
            self.session.close()
            logging.info("🔌 API Session 已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()