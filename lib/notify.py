import requests
import os
import argparse
import logging
import datetime
from typing import Optional

# 配置日志
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DingTalkNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.headers = {"Content-Type": "application/json"}

    def send_msg(self, status: str, pipeline_url: str, report_url: str = None):
        """
        发送钉钉通知
        :param status: 构建状态 (success/failed)
        :param pipeline_url: 流水线链接
        :param report_url: 在线测试报告链接
        """
        if not self.webhook_url:
            logging.warning("⚠️ Webhook URL 为空，跳过发送通知")
            return

        # 样式配置
        if status.lower() == 'success':
            title = "🎉 自动化测试通过"
            color_text = "#### <font color=#00B42A>构建成功</font>"
        else:
            title = "❌ 自动化测试失败"
            color_text = "#### <font color=#FF0000>构建失败</font>"

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 构建报告链接部分 Markdown
        report_link_md = ""
        if report_url:
             report_link_md = f"- **在线报告**: [点击查看图表]({report_url})"

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"""
{color_text}
---
- **项目名称**: Titan-Test
- **结束时间**: {current_time}
- **流水线链接**: [查看 Console]({pipeline_url})
{report_link_md}
---
> 来自 GitLab/GitHub CI 自动推送
                """
            }
        }

        try:
            resp = requests.post(self.webhook_url, json=data, headers=self.headers, timeout=10)
            resp.raise_for_status()

            res_json = resp.json()
            if res_json.get("errcode") == 0:
                logging.info("✅ 钉钉通知发送成功")
            else:
                logging.error(f"⚠️ 钉钉返回错误: {res_json.get('errmsg')}")

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ 发送通知请求异常: {e}")
        except Exception as e:
            logging.error(f"❌ 发送通知未知异常: {e}")


def main():
    parser = argparse.ArgumentParser(description="发送 CI 通知到钉钉")
    parser.add_argument("status", type=str, help="构建状态 (success/failed)")
    args = parser.parse_args()

    # 从环境变量获取配置
    webhook = os.environ.get("NOTIFY_WEBHOOK")
    pipeline_url = os.environ.get("CI_PIPELINE_URL", "http://localhost")
    report_url = os.environ.get("REPORT_URL") # 新增获取报告地址

    if not webhook:
        logging.warning("⚠️ 未配置 NOTIFY_WEBHOOK 环境变量，取消发送")
        return

    notifier = DingTalkNotifier(webhook)
    notifier.send_msg(args.status, pipeline_url, report_url)


if __name__ == "__main__":
    main()