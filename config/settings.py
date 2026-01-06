# config/settings.py
import os
import yaml
import logging

# 1. 获取当前项目的根目录
# (这样无论你在哪里运行命令，都能找到文件)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. 读取环境变量 'ENV'，如果没有设置，默认用 'dev'
# 这里的 'ENV' 就是我们在 Docker 里可以通过 -e 传入的参数
target_env = os.environ.get("ENV", "dev")

# 3. 读取 YAML 文件
config_path = os.path.join(BASE_DIR, "config", "env.yaml")

with open(config_path, "r", encoding="utf-8") as f:
    raw_config = yaml.safe_load(f)

# 4. 拿到最终的配置字典
# 如果 target_env 是 'dev'，就只取 yaml 里 dev 下面的内容
config = raw_config.get(target_env)
logging.basicConfig(level=logging.INFO)
logging.info(f"👻 当前环境: {target_env} | Base URL: {config['base_url']}")

# print(f"👻 当前运行环境: {target_env}, Base URL: {config['base_url']}")