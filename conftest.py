# tests/conftest.py
import pytest
from lib.api_client import ApiClient
from config.settings import config
import logging


# scope="session" 表示整个测试过程中只执行一次登录
# 如果你想每个用例都重新登录，就改成 scope="function"
@pytest.fixture(scope="session")
def auth_client():
    logging.info("🔐 --- 开始执行全局登录 ---")

    # 1. 初始化客户端
    client = ApiClient()

    # 2. 调用登录接口 (这里我们用 httpbin 模拟登录操作)
    # 假设登录接口是 /post，需要传用户名密码
    login_url = f"{config['base_url'].rstrip('/')}/post"
    payload = {"username": "admin", "password": "123"}

    res = client.send_request("post", login_url, json=payload)

    # 3. 模拟提取 Token
    # 在真实项目中，可能是 token = res.json()['data']['token']
    # 这里 httpbin 会把我们要发的 json 原样返回，假装它是 token
    fake_token = "titan-token-123456"
    logging.info(f"🔑 获取 Token 成功: {fake_token}")

    # 4. 【关键步骤】把 Token 设置到 session 的公共头里
    # 这样以后用这个 client 发的所有请求，都会自动带上这个头！
    client.session.headers.update({"Authorization": f"Bearer {fake_token}"})

    # 5. 把在这个“带证上岗”的 client 返回给测试用例
    yield client

    logging.info("🚪 --- 测试结束，清理会话 ---")