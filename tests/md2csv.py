import re
import csv
import os
import argparse


def convert_md_file_to_csv(input_path, output_path=None):
    # 1. 检查文件是否存在
    if not os.path.exists(input_path):
        print(f"错误: 找不到文件 '{input_path}'")
        return

    # 2. 如果未指定输出路径，则默认使用原文件名
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + ".csv"

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # 3. 解析 Markdown 表格
        lines = md_content.strip().split('\n')
        table_data = []

        for line in lines:
            clean_line = line.strip()
            # 匹配典型的 Markdown 表格行：以 | 开始并以 | 结束
            if clean_line.startswith('|') and clean_line.endswith('|'):
                # 剔除分割线行 (如 |---|---|)
                if re.match(r'^\|[\s\-|:|]+\|$', clean_line):
                    continue

                # 提取单元格数据并清洗多余空格
                # 使用 [1:-1] 去掉前后的 |，再按 | 分割
                cells = [cell.strip() for cell in clean_line[1:-1].split('|')]
                table_data.append(cells)

        # 4. 写入 CSV
        if not table_data:
            print("警告: 未在文件中识别到有效的 Markdown 表格。")
            return

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)  # 自动处理内容中的逗号
            writer.writerows(table_data)

        print(f"成功！已将测试用例保存至: {output_path}")

    except Exception as e:
        print(f"转换过程中发生错误: {e}")


if __name__ == "__main__":
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="将包含测试用例的 Markdown 文件转换为 CSV")
    parser.add_argument("input", help="输入的 Markdown 文件路径 (例如: cases.md)")
    parser.add_argument("-o", "--output", help="输出的 CSV 文件路径 (可选)")

    args = parser.parse_args()
    convert_md_file_to_csv(args.input, args.output)