import pytest
import logging
import sys
import os
import platform  # 👈 新增导入
from api.auth_api import AuthApi
from config.settings import config

# ... (路径修复代码保持不变) ...
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# --- 📌 优化点：自动生成 allure 环境信息 ---
@pytest.fixture(scope="session", autouse=True)
def add_allure_environment_property(request):
    """
    在测试结束后，向 allure-results 目录写入 environment.properties
    """
    # 确保 allure-results 目录存在
    allure_dir = "allure-results"
    if not os.path.exists(allure_dir):
        os.makedirs(allure_dir)

    env_info = {
        "System": platform.system(),
        "Python Version": platform.python_version(),
        "Project": "Titan-Test",
        "Target Env": os.environ.get("ENV", "dev"),
        "Base URL": config.get("base_url", "unknown")
    }

    env_file = os.path.join(allure_dir, "environment.properties")
    with open(env_file, "w", encoding="utf-8") as f:
        for key, value in env_info.items():
            f.write(f"{key}={value}\n")


# ----------------------------------------

@pytest.fixture(scope="session")
def auth_client():
    # ... (原有的 fixture 代码保持不变) ...
    logging.info("🔐 --- 全局登录初始化 ---")
    api = AuthApi()
    user_conf = config.get('auth', {})
    username = user_conf.get('username', 'default_user')
    password = user_conf.get('password', 'default_pass')
    logging.info(f"👤 使用账号登录: {username}")
    res = api.login(username, password)
    fake_token = "titan-token-123456"
    api.session.headers.update({"Authorization": f"Bearer {fake_token}"})
    yield api
    logging.info("🚪 --- 测试会话结束，正在清理资源 ---")
    api.close()