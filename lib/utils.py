# lib/utils.py
import yaml
import os


def load_yaml_data(file_path):
    """
    读取 YAML 文件并返回 Python 对象
    :param file_path: 比如 'data/login_cases.yaml'
    :return: List 或 Dict
    """
    # 拼接绝对路径，确保在哪运行都能找到文件
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, file_path)

    with open(full_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)