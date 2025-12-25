# tests/test_orders.py
import logging


def test_create_order(auth_client):
    """
    这个测试用例依赖 auth_client，所以它执行前会自动先去登录
    """
    # 这里我们访问 httpbin 的 /bearer 接口
    # 这个接口专门用来检测 Authorization 头是否正确
    # 如果头里没有 Token，这个接口会报错
    url = "https://httpbin.org/bearer"

    logging.info("🛒 正在尝试创建订单 (访问需鉴权接口)...")

    # 直接发请求，不用管 Header，auth_client 已经自动带上了
    res = auth_client.send_request("get", url)

    # 断言我们真的带上了 Token
    assert res.status_code == 200
    assert res.json()['authenticated'] == True
    assert res.json()['token'] == "titan-token-123456"

    logging.info("✅ 鉴权成功！订单创建流程通过。")