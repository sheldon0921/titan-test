import pytest
import logging
import sys
import os
import platform
from api.auth_api import AuthApi
from config.settings import config

# 将项目根目录加入 python path，防止导包错误
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


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


@pytest.fixture(scope="session")
def auth_client():
    """
    全局鉴权 Fixture
    逻辑：优先读取配置文件中的 token，如果存在则跳过登录；否则使用账号密码登录。
    """
    logging.info("🔐 --- 全局登录初始化 ---")
    api = AuthApi()

    # 获取 config/env.yaml 中的 auth 配置部分
    auth_conf = config.get('auth', {})

    # 1. 尝试读取 Token
    token = auth_conf.get('token')

    if token:
        # ✅ 场景 A：配置文件里有 Token -> 直接注入，跳过登录
        # 只显示前15位，保护隐私
        logging.info(f"🎫 检测到配置文件 Token: {token[:15]}******")
        logging.info("🚀 跳过登录接口调用，直接使用配置 Token")

        # 将 Token 更新到 Session Header 中
        # 注意：这里假设后端使用的是 Authorization: Bearer <token> 格式
        api.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
    else:
        # ✅ 场景 B：配置文件里没 Token -> 走正常的账号密码登录流程
        username = auth_conf.get('username', 'default_user')
        password = auth_conf.get('password', 'default_pass')
        logging.info(f"👤 未配置 Token，尝试使用账号登录: {username}")

        try:
            # 调用登录接口
            # 注意：实际项目中 login 方法通常返回 response，需要从中提取 token
            api.login(username, password)

            # 模拟：由于这里使用的是 httpbin 并没有真实返回 token
            # 我们手动注入一个 fake_token 模拟登录成功后的状态
            # 在真实业务代码中，应该是：token = res.json()['data']['token']
            fake_token = "titan-token-123456"
            api.session.headers.update({"Authorization": f"Bearer {fake_token}"})

        except Exception as e:
            logging.error(f"❌ 登录失败: {e}")
            # 如果鉴权是强依赖，建议在这里 raise e 终止测试，否则后面的用例都会挂

    yield api

    logging.info("🚪 --- 测试会话结束，正在清理资源 ---")
    api.close()