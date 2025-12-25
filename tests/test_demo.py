# tests/test_demo.py
from config.settings import config
from lib.api_client import ApiClient  # 导入我们的新工具

# 实例化一次，或者放在 pytest 的 fixture 里（以后会教你）
client = ApiClient()


def test_environment_connection():
    # 拼接完整的 URL
    # rstrip('/') 是防止配置里多写了个斜杠导致 URL 变成 //
    base_url = config['base_url'].rstrip('/')
    target_url = f"{base_url}/get"  # 假设我们要访问 /get 这个接口

    # --- 现在的调用方式 ---
    # 我们不再关心怎么打印日志，怎么处理异常，只管发命令
    res = client.send_request("get", target_url)

    # 断言
    assert res.status_code == 200
    # 还可以顺便校验一下返回的 json 数据
    assert res.json()['url'] == target_url