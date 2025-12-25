# lib/notify.py
import requests
import os
import sys
import datetime


def send_dingtalk_msg(webhook_url, status, pipeline_url):
    """
    发送钉钉通知
    """
    # 根据状态决定标题颜色和内容
    if status == 'success':
        title = "🎉 自动化测试通过"
        color_text = "#### <font color=#00B42A>构建成功</font>"
    else:
        title = "❌ 自动化测试失败"
        color_text = "#### <font color=#FF0000>构建失败</font>"

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 组装 markdown 格式的消息
    # 钉钉支持 markdown，可以做得很好看
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": f"""
{color_text}
---
- **项目名称**: Titan-Test
- **结束时间**: {current_time}
- **流水线链接**: [点击查看详情]({pipeline_url})
---
> 来自 GitLab CI 自动推送
            """
        }
    }

    try:
        res = requests.post(webhook_url, json=data)
        if res.json().get("errcode") == 0:
            print("✅ 通知发送成功")
        else:
            print(f"⚠️ 通知发送失败: {res.text}")
    except Exception as e:
        print(f"❌ 发送异常: {e}")


if __name__ == "__main__":
    # 从命令行参数获取状态 (success/failed)
    # sys.argv[1] 是我们在命令行传进来的第一个参数
    if len(sys.argv) < 2:
        print("需要传入状态参数: success 或 failed")
        sys.exit(1)

    status = sys.argv[1]

    # 从环境变量获取配置 (安全！)
    webhook = os.environ.get("NOTIFY_WEBHOOK")
    pipeline_url = os.environ.get("CI_PIPELINE_URL", "http://localhost")

    if not webhook:
        print("⚠️ 未配置 Webhook URL，跳过发送通知")
    else:
        send_dingtalk_msg(webhook, status, pipeline_url)