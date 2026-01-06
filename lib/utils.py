import yaml
import os
import jsonpath # 需在 requirements.txt 添加 jsonpath

# ...保留原有 load_yaml_data...

def get_json_value(response_json, expr):
    """
    使用 JsonPath 提取数据
    :param response_json: 响应的字典对象
    :param expr: jsonpath 表达式 (如 '$.data.token')
    :return: 提取到的值 (如果是列表且只有一个元素，自动解包)
    """
    res = jsonpath.jsonpath(response_json, expr)
    if res:
        return res[0] if len(res) == 1 else res
    return None