import yaml
import logging
import jsonpath
from pathlib import Path
from typing import Any, Dict, List, Union

def load_yaml_data(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    读取 YAML 文件数据
    :param file_path: 相对项目根目录的文件路径 (如 'data/login_cases.yaml')
    :return: 字典列表
    """
    # 获取项目根目录 (假设 utils.py 在 lib/ 下，根目录在 lib 的上一级)
    base_dir = Path(__file__).resolve().parent.parent
    full_path = base_dir / file_path

    if not full_path.exists():
        logging.error(f"❌ 测试数据文件不存在: {full_path}")
        raise FileNotFoundError(f"测试数据文件不存在: {full_path}")

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, list):
                logging.error(f"❌ YAML 数据格式错误: 期望列表格式，实际为 {type(data).__name__}")
                return []
            return data if data else []
    except yaml.YAMLError as e:
        logging.error(f"❌ YAML 格式错误: {e}")
        raise ValueError(f"YAML 格式错误: {e}") from e
    except Exception as e:
        logging.error(f"❌ 读取文件异常: {e}")
        raise RuntimeError(f"读取文件异常: {e}") from e

def get_json_value(response_json: Dict, expr: str, default: Any = None) -> Any:
    """
    使用 JsonPath 提取数据
    :param response_json: 响应的字典对象
    :param expr: jsonpath 表达式 (如 '$.data.token')
    :param default: 未找到时返回的默认值
    :return: 提取到的值 (如果是列表且只有一个元素，自动解包；否则返回 default)
    """
    if not response_json or not isinstance(response_json, dict):
        logging.warning(f"⚠️ response_json 必须是字典类型，实际: {type(response_json).__name__}")
        return default

    if not expr or not isinstance(expr, str):
        logging.warning("⚠️ jsonpath 表达式必须是非空字符串")
        return default

    try:
        res = jsonpath.jsonpath(response_json, expr)
        if res:
            return res[0] if len(res) == 1 else res
        return default
    except Exception as e:
        logging.error(f"❌ JsonPath 提取异常: expr={expr}, error={e}")
        return default