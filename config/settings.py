import os
import yaml
import logging

# 获取当前项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 读取环境变量
target_env = os.environ.get("ENV", "dev")

# 读取 YAML 文件
config_path = os.path.join(BASE_DIR, "config", "env.yaml")

if not os.path.exists(config_path):
    raise FileNotFoundError(f"配置文件未找到: {config_path}")

with open(config_path, "r", encoding="utf-8") as f:
    raw_config = yaml.safe_load(f)

# 获取环境配置，如果没找到则返回空字典，防止报错
config = raw_config.get(target_env, {})

# 初始化日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f"👻 当前环境: {target_env} | Base URL: {config.get('base_url', 'Not Set')}")