import logging
import allure


@allure.feature("订单模块")
class TestOrders:

    @allure.story("创建订单前鉴权")
    def test_create_order(self, auth_client):
        """
        auth_client 是在 conftest.py 里实例化的 AuthApi 对象
        """
        logging.info("🛒 正在尝试创建订单 (访问需鉴权接口)...")

        # ✅ 优化：直接调用封装好的业务方法，不再手写 URL
        # auth_client 已经是 AuthApi 的实例了
        res = auth_client.check_auth()

        # 断言
        assert res.status_code == 200
        assert res.json()['authenticated'] is True
        # 验证 Token 是否是我们登录时伪造的那个
        assert res.json()['token'] == "titan-token-123456"

        logging.info("✅ 鉴权成功！订单创建流程通过。")