import requests
import logging
import allure
import urllib3  # 👈 导入这个库
from config.settings import config  # 导入配置
# 禁用安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        # 从配置中读取默认超时时间，如果没有则默认为 10秒
        self.timeout = config.get("timeout", 10)

    def send_request(self, method, url, **kwargs):
        # 1. 自动注入超时时间 (如果在 kwargs 里没传，就用默认的)
        kwargs.setdefault("timeout", self.timeout)

        # 2. 禁用 SSL 警告 (如果是内网测试很有用)
        kwargs.setdefault("verify", False)

        with allure.step(f"🚀 API请求: {method.upper()} {url}"):
            logging.info(f"🚀 发送请求 >>> {method.upper()} {url}")
            # ... (保留您原有的 allure attach 逻辑) ...

            try:
                response = self.session.request(method, url, **kwargs)
                logging.info(f"✅ 响应状态: {response.status_code} | 耗时: {response.elapsed.total_seconds()}s")

                # 优化: 只有在非 200 响应时才 attach 响应体，或者截取更长
                if response.status_code >= 400:
                    allure.attach(response.text[:2000], name="错误响应内容",
                                  attachment_type=allure.attachment_type.TEXT)

                return response
            except Exception as e:
                logging.error(f"❌ 请求异常: {e}")
                allure.attach(str(e), name="异常堆栈", attachment_type=allure.attachment_type.TEXT)
                raise e

    # 3. 增加语法糖方法，让测试用例写起来更短
    def get(self, url, **kwargs):
        return self.send_request("get", url, **kwargs)

    def post(self, url, **kwargs):
        return self.send_request("post", url, **kwargs)