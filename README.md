Titan-Test 接口自动化测试框架

基于 Pytest + Requests + Allure + Docker 构建的轻量级接口自动化测试框架。

📊 测试报告可视化

本项目已集成 GitHub Pages，每次代码提交或定时运行后，会自动生成在线测试报告。

在线查看 (CI/CD)

进入 GitHub 仓库的 Actions 页面查看运行日志。

运行结束后，钉钉群机器人会推送通知，点击通知中的 [在线报告] 链接即可。

或者直接访问：https://<你的GitHub用户名>.github.io/titan-test/ 查看最新报告。

首次配置说明：

确保在仓库 Settings -> Pages 中，将 Source 设置为 gh-pages 分支（该分支会在第一次 CI 运行成功后自动创建）。

本地查看

如果你在本地运行了测试：

# 1. 运行测试并生成数据
pytest --alluredir=./allure-results

# 2. 启动本地服务查看报告 (需要安装 Allure 命令行工具)
allure serve ./allure-results


📂 项目结构

titan-test/
├── .github/workflows/  # CI/CD 配置 (包含 Allure 报告生成)
├── api/                # API 封装层
├── config/             # 配置文件
├── data/               # 测试数据
├── lib/                # 工具库 (notify.py 已升级支持报告链接)
├── allure-results/     # (自动生成) 存放测试原始 JSON 数据
├── tests/              # 测试用例
├── conftest.py         # Pytest Fixture
└── requirements.txt    # 依赖


🚀 快速开始

安装依赖

pip install -r requirements.txt


运行测试

pytest

