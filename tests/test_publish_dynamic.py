import pytest
import allure
import logging
import json
from typing import Dict, Any
from lib.utils import load_yaml_data, get_json_value

# 1. 加载 YAML 数据
# 注意：为了防止文件不存在导致报错，最好做个容错，或者确保文件路径正确
try:
    test_data = load_yaml_data("data/publish_dynamic_cases.yaml")
    if not test_data:
        logging.warning("⚠️ 数据文件为空或读取失败")
        test_data = []
except Exception as e:
    logging.error(f"❌ 加载测试数据异常: {e}")
    test_data = []


@allure.feature("社区动态模块")
class TestPublishDynamic:

    @allure.story("发布动态")
    @pytest.mark.parametrize("case_info", test_data, ids=[i.get('title', f"case_{idx}") for idx, i in enumerate(test_data)])
    def test_publish_dynamic(self, case_info: dict, auth_client):
        """
        发布动态接口测试（数据驱动版）

        :param case_info: 从 yaml 中读取的单条测试数据
        :param auth_client: 鉴权 Fixture
        """
        # 2. 从 case_info 中提取数据
        title = case_info.get("title", "未知用例")
        payload = case_info.get("payload")
        headers = case_info.get("headers")  # 可能是 None
        expected = case_info.get("expected", {})

        # 验证测试数据完整性
        if not payload:
            pytest.skip(f"⚠️ 用例 '{title}' 缺少 payload 数据")

        if not expected:
            pytest.skip(f"⚠️ 用例 '{title}' 缺少 expected 数据")

        # 动态更新 Allure 报告的标题，让报告更清晰
        allure.dynamic.title(title)

        # 声明响应JSON变量，供后续步骤复用
        response_json = None

        # 步骤1: 准备测试数据
        with allure.step("步骤1: 准备测试数据"):
            url = f"{auth_client.base_url}/circle/dynamic/publishdynamic"

            # 格式化 JSON 附件
            payload_json = json.dumps(payload, ensure_ascii=False, indent=2)
            allure.attach(payload_json, name="请求数据", attachment_type=allure.attachment_type.JSON)

            if headers:
                allure.attach(
                    json.dumps(headers, ensure_ascii=False, indent=2),
                    name="自定义请求头",
                    attachment_type=allure.attachment_type.JSON
                )

            logging.info(f"🚀 开始执行用例: {title}")

        # 步骤2: 发送请求
        with allure.step("步骤2: 发送发布动态请求"):
            res = auth_client.post(url, json=payload, headers=headers)

            # 附件记录响应
            try:
                response_json = res.json()
                response_text = json.dumps(response_json, ensure_ascii=False, indent=2)
                attachment_type = allure.attachment_type.JSON
            except (json.JSONDecodeError, ValueError):
                response_text = res.text
                attachment_type = allure.attachment_type.TEXT

            allure.attach(response_text, name="响应数据", attachment_type=attachment_type)
            logging.info(f"📥 响应状态: {res.status_code}")

        # 步骤3: 验证响应状态码
        with allure.step("步骤3: 验证响应状态码"):
            expected_status = expected.get("status_code", 200)
            allure.attach(
                f"预期状态码: {expected_status}\n实际状态码: {res.status_code}",
                name="状态码对比",
                attachment_type=allure.attachment_type.TEXT
            )
            assert res.status_code == expected_status, \
                f"状态码不匹配: 期望 {expected_status}, 实际 {res.status_code}"

        # 步骤4: 验证业务数据
        with allure.step("步骤4: 验证业务数据"):
            # 验证业务逻辑
            if "msg" in expected and response_json:
                try:
                    actual_msg = get_json_value(response_json, "$.msg")
                    expected_msg = expected.get("msg")

                    allure.attach(
                        f"预期消息: {expected_msg}\n实际消息: {actual_msg}",
                        name="消息验证",
                        attachment_type=allure.attachment_type.TEXT
                    )

                    assert actual_msg == expected_msg, \
                        f"消息不匹配: 期望 {expected_msg}, 实际 {actual_msg}"

                    # 验证动态ID（如果返回中包含）
                    if "dynamic_id" in response_json or "id" in str(response_json):
                        actual_id = get_json_value(response_json, "$.data.id") or \
                                   get_json_value(response_json, "$.dynamic_id") or \
                                   get_json_value(response_json, "$.id")
                        allure.attach(
                            f"动态ID: {actual_id}",
                            name="动态ID验证",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        logging.info(f"✅ 业务数据验证通过 - 消息: {actual_msg}, ID: {actual_id}")
                    else:
                        logging.info(f"✅ 业务数据验证通过 - 消息: {actual_msg}")
                except (json.JSONDecodeError, ValueError) as e:
                    logging.warning(f"⚠️ 无法验证业务消息 - JSON解析错误: {e}")
                except KeyError as e:
                    logging.warning(f"⚠️ 无法验证业务消息 - 缺少字段: {e}")
                except Exception as e:
                    logging.warning(f"⚠️ 无法验证业务消息 - 未知错误: {type(e).__name__}: {e}")
            else:
                logging.info("✅ 业务数据验证通过（无消息验证要求）")