"""
Allure Step 使用示例
展示如何在测试用例中添加详细的 Allure 步骤
"""
import pytest
import allure
import logging
from api.auth_api import AuthApi
from lib.utils import get_json_value


@allure.feature("Allure Step 示例")
class TestAllureStepExamples:

    @allure.story("基础 Step 使用")
    def test_basic_step_usage(self):
        """演示基本的 Allure step 使用"""

        # 步骤1: 简单的步骤
        with allure.step("步骤1: 准备测试环境"):
            logging.info("准备测试数据")
            test_data = {"username": "test", "password": "123456"}

        # 步骤2: 在步骤中添加附件
        with allure.step("步骤2: 添加测试数据到报告"):
            # 可以添加文本附件
            allure.attach(
                str(test_data),
                name="测试数据",
                attachment_type=allure.attachment_type.TEXT
            )

            # 可以添加 JSON 附件
            import json
            allure.attach(
                json.dumps(test_data, ensure_ascii=False, indent=2),
                name="JSON格式数据",
                attachment_type=allure.attachment_type.JSON
            )

        # 步骤3: 在步骤中添加关键信息
        with allure.step("步骤3: 记录关键信息"):
            allure.parameter("用户名", test_data["username"])
            allure.parameter("密码长度", len(test_data["password"]))
            logging.info("关键信息已记录到报告")

        # 步骤4: 验证结果
        with allure.step("步骤4: 验证结果"):
            assert test_data["username"] == "test"
            allure.attach("断言通过", name="验证结果", attachment_type=allure.attachment_type.TEXT)

    @allure.story("嵌套 Step 使用")
    def test_nested_steps(self):
        """演示嵌套步骤的使用"""

        with allure.step("主步骤1: 用户注册流程"):
            with allure.step("子步骤1.1: 验证用户信息"):
                username = "testuser"
                password = "123456"
                email = "test@example.com"
                allure.attach(
                    f"用户名: {username}\n邮箱: {email}",
                    name="用户信息",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("子步骤1.2: 发送注册请求"):
                # 模拟发送请求
                logging.info("发送注册请求...")
                allure.attach("POST /api/register", name="请求方法", attachment_type=allure.attachment_type.TEXT)

            with allure.step("子步骤1.3: 验证注册结果"):
                assert True
                allure.attach("注册成功", name="结果", attachment_type=allure.attachment_type.TEXT)

        with allure.step("主步骤2: 用户登录流程"):
            with allure.step("子步骤2.1: 使用注册的账号登录"):
                logging.info("登录中...")

            with allure.step("子步骤2.2: 验证登录状态"):
                assert True

    @allure.story("API 测试中的 Step")
    def test_api_with_steps(self):
        """演示在 API 测试中如何使用步骤"""

        auth_api = AuthApi()

        try:
            # 步骤1: 初始化测试环境
            with allure.step("步骤1: 初始化测试环境"):
                allure.attach(
                    f"Base URL: {auth_api.base_url}",
                    name="测试环境",
                    attachment_type=allure.attachment_type.TEXT
                )

            # 步骤2: 执行登录操作
            with allure.step("步骤2: 执行登录操作"):
                username = "admin"
                password = "123"

                allure.attach(
                    f"用户名: {username}\n密码: {'*' * len(password)}",
                    name="登录凭证",
                    attachment_type=allure.attachment_type.TEXT
                )

                res = auth_api.login(username, password)

            # 步骤3: 验证响应
            with allure.step("步骤3: 验证响应状态"):
                allure.attach(
                    f"状态码: {res.status_code}",
                    name="HTTP状态码",
                    attachment_type=allure.attachment_type.TEXT
                )

                with allure.step("步骤3.1: 检查状态码是否为 200"):
                    assert res.status_code == 200
                    allure.attach(
                        "状态码验证通过",
                        name="验证结果",
                        attachment_type=allure.attachment_type.TEXT
                    )

            # 步骤4: 验证响应数据
            with allure.step("步骤4: 验证响应数据"):
                try:
                    response_data = res.json()

                    # 添加完整的 JSON 响应
                    import json
                    allure.attach(
                        json.dumps(response_data, ensure_ascii=False, indent=2),
                        name="完整响应",
                        attachment_type=allure.attachment_type.JSON
                    )

                    # 提取特定字段
                    actual_user = get_json_value(response_data, "$.json.username")

                    with allure.step("步骤4.1: 验证用户名"):
                        allure.attach(
                            f"预期: {username}\n实际: {actual_user}",
                            name="用户名对比",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        assert actual_user == username

                except Exception as e:
                    allure.attach(
                        f"JSON解析失败: {str(e)}",
                        name="错误信息",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    raise

        finally:
            # 清理步骤
            with allure.step("清理: 关闭连接"):
                auth_api.close()
                logging.info("测试资源已清理")

    @allure.story("断言失败的 Step")
    def test_assertion_failure_with_step(self):
        """演示断言失败时步骤的记录"""

        with allure.step("步骤1: 执行测试"):
            actual_value = 100
            expected_value = 200

            with allure.step("步骤1.1: 对比值"):
                allure.attach(
                    f"预期值: {expected_value}\n实际值: {actual_value}",
                    name="值对比",
                    attachment_type=allure.attachment_type.TEXT
                )

                # 这个断言会失败，用于演示
                assert actual_value == expected_value, \
                    f"值不匹配: 预期 {expected_value}, 实际 {actual_value}"

    @allure.story("使用 Allure 参数")
    @pytest.mark.parametrize("username,password", [
        ("user1", "pass1"),
        ("user2", "pass2"),
        ("user3", "pass3")
    ])
    def test_with_allure_parameters(self, username, password):
        """演示 Allure 参数的使用"""

        allure.parameter("用户名", username)
        allure.parameter("密码长度", len(password))

        with allure.step(f"测试用户 {username}"):
            allure.attach(
                f"用户名: {username}\n密码: {'*' * len(password)}",
                name="登录信息",
                attachment_type=allure.attachment_type.TEXT
            )
            assert len(username) > 0
            assert len(password) > 0
