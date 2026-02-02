from typing import Optional
import allure
import requests
from lib.api_client import ApiClient
from config.settings import config


class AuthApi(ApiClient):
    """
    用户认证模块接口封装
    """

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        super().__init__()
        if session:
            self.session = session
        # 统一管理该模块的 Path
        self.base_url = str(config.get('base_url', '')).rstrip('/')

    @allure.step("执行用户登录: {username}")
    def login(self, username: str, password: str) -> requests.Response:
        """
        登录接口
        :param username: 用户名
        :param password: 密码
        :return: 响应对象
        """
        url = f"{self.base_url}/post"
        payload = {"username": username, "password": password}
        # 直接调用父类的 send_request
        return self.send_request("post", url, json=payload)

    @allure.step("检查Token有效性")
    def check_auth(self) -> requests.Response:
        """
        鉴权验证接口
        :return: 响应对象
        """
        url = f"{self.base_url}/bearer"
        return self.send_request("get", url)