# Titan-Test 接口自动化测试框架

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Pytest](https://img.shields.io/badge/pytest-7.0+-yellow)

基于 Pytest + Requests + Allure + Docker 构建的轻量级接口自动化测试框架。采用 API Object 分层设计模式，支持多环境切换、数据驱动测试及 CI/CD 集成。

## 📂 项目结构

```text
titan-test/
├── api/                # API 封装层 (API Object)
│   └── auth_api.py     # 认证模块接口
├── config/             # 配置文件
│   ├── env.yaml        # 多环境配置 (Dev/Prod)
│   └── settings.py     # 配置加载逻辑
├── data/               # 测试数据
│   └── login_cases.yaml
├── lib/                # 公共工具库
│   ├── api_client.py   # HTTP 请求基类 (Session, Log, Allure)
│   ├── db_utils.py     # 数据库操作工具
│   ├── notify.py       # 消息通知 (钉钉/飞书)
│   └── utils.py        # 通用工具 (YAML读取, JSONPath提取)
├── reports/            # 测试报告 (自动生成)
├── tests/              # 测试用例
│   ├── test_login_ddt.py  # 数据驱动登录测试
│   └── test_orders.py     # 依赖登录状态的业务测试
├── conftest.py         # Pytest 共享夹具 (Fixture)
├── pytest.ini          # Pytest 运行配置
├── Dockerfile          # Docker 构建文件
└── requirements.txt    # 项目依赖