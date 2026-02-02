import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# 1. 优化：使用 Pathlib 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 读取环境变量，并添加验证
target_env = os.environ.get("ENV", "dev")
VALID_ENVS = ["dev", "prod", "staging", "test"]  # 支持的环境列表

if target_env not in VALID_ENVS:
    logging.warning(f"⚠️ 环境变量 ENV='{target_env}' 不在预定义列表中，可能存在问题")
    logging.warning(f"💡 可用环境: {', '.join(VALID_ENVS)}")

# 2. 优化：路径拼接更优雅
config_path = BASE_DIR / "config" / "env.yaml"

if not config_path.exists():
    raise FileNotFoundError(f"配置文件未找到: {config_path}")

try:
    with open(config_path, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)
except FileNotFoundError as e:
    raise FileNotFoundError(f"配置文件不存在: {config_path}") from e
except yaml.YAMLError as e:
    raise ValueError(f"配置文件格式错误: {config_path} - {e}") from e
except Exception as e:
    raise RuntimeError(f"读取配置文件失败: {config_path} - {e}") from e

if not raw_config:
    raise ValueError(f"配置文件为空: {config_path}")

# 获取环境配置
config: Dict[str, Any] = raw_config.get(target_env, {})
if not config:
    available_envs = ", ".join(raw_config.keys()) if raw_config else "无"
    raise ValueError(f"环境配置 '{target_env}' 不存在，可用环境: {available_envs}")

# 验证必需的配置项
required_keys = ["base_url"]
missing_keys = [key for key in required_keys if key not in config]
if missing_keys:
    logging.warning(f"⚠️ 环境配置 '{target_env}' 缺少必需的配置项: {', '.join(missing_keys)}")

# 初始化日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.info(f"👻 当前环境: {target_env} | Base URL: {config.get('base_url', 'Not Set')}")