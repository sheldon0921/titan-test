# api/auth_api.py
from lib.api_client import ApiClient
from config.settings import config


class AuthApi(ApiClient):
    """
    用户认证模块接口封装
    """

    def __init__(self, session=None):
        super().__init__()
        if session:
            self.session = session
        # 统一管理该模块的 Path
        self.base_url = config['base_url'].rstrip('/')

    def login(self, username, password):
        """
        登录接口
        """
        url = f"{self.base_url}/post"  # 假设登录是 /post
        payload = {"username": username, "password": password}
        # 直接调用父类的 send_request
        return self.send_request("post", url, json=payload)


    def check_auth(self):
        """
        鉴权验证接口
        """
        # ❌ 不要写死: url = "https://httpbin.org/bearer"
        # ✅ 使用拼接: 这样会根据 config/env.yaml 自动切换环境
        url = f"{self.base_url}/bearer"
        return self.send_request("get", url)