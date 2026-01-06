import pytest
from api.auth_api import AuthApi
import logging


@pytest.fixture(scope="session")
def auth_client():
    """
    执行全局登录，并返回一个已经带了 Token 的 AuthApi 对象
    """
    logging.info("🔐 --- 全局登录初始化 ---")

    # 实例化业务对象
    api = AuthApi()

    # 执行登录 (这里使用硬编码账号或从 env 获取)
    # 实际项目中，建议将账号密码放在 config/env.yaml 或 环境变量中
    res = api.login("admin", "123")

    # 模拟提取 Token (根据您的 httpbin 逻辑)
    # 真实场景：token = res.json()['data']['token']
    fake_token = "titan-token-123456"

    # 将 Token 更新到 session headers 中
    # 这样后续复用这个 api 对象的 session 时，都会带上 Authorization
    api.session.headers.update({"Authorization": f"Bearer {fake_token}"})

    yield api  # 返回封装好的 API 对象，而不是底层的 client

    logging.info("🚪 --- 测试会话结束 ---")