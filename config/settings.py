import os
import yaml
import logging
from pathlib import Path  # 引入 Pathlib

# 1. 优化：使用 Pathlib 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 读取环境变量
target_env = os.environ.get("ENV", "dev")

# 2. 优化：路径拼接更优雅
config_path = BASE_DIR / "config" / "env.yaml"

if not config_path.exists():
    raise FileNotFoundError(f"配置文件未找到: {config_path}")

try:
    with open(config_path, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)
except yaml.YAMLError as e:
    raise ValueError(f"配置文件格式错误: {e}")

# 获取环境配置
config = raw_config.get(target_env, {})

# 初始化日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f"👻 当前环境: {target_env} | Base URL: {config.get('base_url', 'Not Set')}")