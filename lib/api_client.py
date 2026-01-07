import requests
import logging
import allure
import urllib3
from typing import Optional, Dict, Any  # 引入类型提示
from config.settings import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.timeout = config.get("timeout", 10)

    def send_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        发送 HTTP 请求的通用方法
        :param method: 请求方法 (GET, POST...)
        :param url: 请求地址
        :param kwargs: requests 支持的其他参数 (params, json, headers...)
        :return: Response 对象
        """
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("verify", False)

        # 优化：打印更详细的 Header 信息以便调试（仅在 Debug 模式）
        # logging.debug(f"Headers: {kwargs.get('headers')}")

        with allure.step(f"🚀 API请求: {method.upper()} {url}"):
            logging.info(f"🚀 发送请求 >>> {method.upper()} {url}")

            try:
                response = self.session.request(method, url, **kwargs)

                # 优化：状态码日志颜色区分（如果是支持颜色的控制台）
                log_msg = f"✅ 响应状态: {response.status_code} | 耗时: {response.elapsed.total_seconds()}s"
                if response.status_code >= 400:
                    logging.error(log_msg)
                else:
                    logging.info(log_msg)

                # 错误处理逻辑保留...
                if response.status_code >= 400:
                    allure.attach(response.text[:2000], name="错误响应内容",
                                  attachment_type=allure.attachment_type.TEXT)

                return response
            except Exception as e:
                logging.error(f"❌ 请求异常: {e}")
                allure.attach(str(e), name="异常堆栈", attachment_type=allure.attachment_type.TEXT)
                raise e

    # 类型提示让调用更清晰
    def get(self, url: str, **kwargs) -> requests.Response:
        return self.send_request("get", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self.send_request("post", url, **kwargs)