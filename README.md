# 🚀 Titan Automated Test Framework

**Titan-Test** 是一个基于 **Python** 和 **Pytest** 构建的轻量级自动化测试框架。它集成了 **Requests** 进行接口测试，使用 **Allure** 生成可视化测试报告，支持 **MySQL** 数据库断言，并包含 **GitHub Actions** 和 **GitLab CI** 的持续集成配置。

---

## 🛠️ 技术栈 (Tech Stack)

* **语言**: Python 3.9+
* **测试框架**: Pytest
* **HTTP 请求**: Requests
* **测试报告**: Allure
* **数据驱动**: PyYAML (YAML)
* **数据提取**: JsonPath
* **数据库操作**: PyMySQL
* **容器化**: Docker
* **CI/CD**: GitHub Actions / GitLab CI

---

## 📂 项目结构 (Project Structure)

```text
titan-test/
├── .github/workflows/   # GitHub Actions CI 配置
├── api/                 # 业务接口封装 (API Object 模式)
├── config/              # 配置文件 (环境配置、全局设置)
├── data/                # 测试数据 (YAML 格式)
├── lib/                 # 公共工具库 (APIClient, DBUtils, Notify 等)
├── tests/               # 测试用例目录
├── .gitignore           # Git 忽略配置
├── .gitlab-ci.yml       # GitLab CI 配置
├── conftest.py          # Pytest 共享 Fixture 和 钩子函数
├── Dockerfile           # Docker 镜像构建文件
├── pytest.ini           # Pytest 配置文件
├── requirements.txt     # 项目依赖列表
└── README.md            # 项目说明文档