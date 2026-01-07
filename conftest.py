import pytest
import logging
import sys
import os
from api.auth_api import AuthApi
from config.settings import config # 导入配置

# 1. 路径修复 (保持您之前的修复)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def auth_client():
    """
    执行全局登录，并返回一个已经带了 Token 的 AuthApi 对象
    """
    logging.info("🔐 --- 全局登录初始化 ---")

    # 实例化业务对象
    api = AuthApi()

    # 2. 从配置中读取账号 (不再硬编码)
    user_conf = config.get('auth', {})
    username = user_conf.get('username', 'default_user')
    password = user_conf.get('password', 'default_pass')

    logging.info(f"👤 使用账号登录: {username}")
    res = api.login(username, password)

    # 模拟提取 Token (这里是为了演示，实际需根据 login 接口返回提取)
    fake_token = "titan-token-123456"

    # 将 Token 更新到 session headers 中
    api.session.headers.update({"Authorization": f"Bearer {fake_token}"})

    yield api

    # 👉 新增：测试结束后清理资源
    logging.info("🚪 --- 测试会话结束，正在清理资源 ---")
    api.close()