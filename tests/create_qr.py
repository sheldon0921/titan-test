import qrcode
from PIL import Image
import os

def create_qr_with_logo(url, logo_path, output_file="qr_with_logo.png"):
    # 1. 检查 Logo 文件是否存在
    if not os.path.exists(logo_path):
        print(f"错误：找不到 Logo 文件 '{logo_path}'，请检查文件名或路径。")
        return

    # 2. 创建二维码对象
    # 关键点：version可以自动调整，但 error_correction 必须是 H (High)，容错率最高(30%)
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 3. 生成二维码图片，并转换为 RGBA 模式（以便处理颜色和透明度）
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    # 4. 打开 Logo 图片
    logo_img = Image.open(logo_path)

    # 5. 计算 Logo 的大小
    # Logo 的宽和高不能超过二维码的 1/4，否则可能扫不出来
    w, h = qr_img.size
    factor = 4  # 缩放比例
    size_w = int(w / factor)
    size_h = int(h / factor)

    # 6. 调整 Logo 大小，使用高质量重采样
    logo_img = logo_img.resize((size_w, size_h), Image.Resampling.LANCZOS)

    # 7. 计算 Logo 粘贴的位置（居中）
    paste_w = int((w - size_w) / 2)
    paste_h = int((h - size_h) / 2)

    # 8. 将 Logo 粘贴到二维码上
    # 第三个参数 logo_img 是作为 mask 使用，如果 Logo 是透明背景 png，这一步很重要
    qr_img.paste(logo_img, (paste_w, paste_h), logo_img if logo_img.mode == 'RGBA' else None)

    # 9. 保存
    qr_img.save(output_file)
    print(f"成功！带 Logo 的二维码已保存为: {output_file}")

# --- 使用示例 ---
# 请修改下面两行：
my_url = "https://mddfiles.oss-cn-shanghai.aliyuncs.com/mdd-back-all/.upload/2025/11/20/b0986fd4-b7e8-44b0-a475-fb07c602b858.jpeg"      # 您的链接
my_logo = "logo.png"                    # 您的图片文件名

create_qr_with_logo(my_url, my_logo)
