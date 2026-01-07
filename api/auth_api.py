import allure
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

    @allure.step("执行用户登录: {username}")
    def login(self, username, password):
        """
        登录接口
        :param username: 用户名
        :param password: 密码
        """
        url = f"{self.base_url}/post"
        payload = {"username": username, "password": password}
        # 直接调用父类的 send_request
        return self.send_request("post", url, json=payload)

    @allure.step("检查Token有效性")
    def check_auth(self):
        """
        鉴权验证接口
        """
        url = f"{self.base_url}/bearer"
        return self.send_request("get", url)