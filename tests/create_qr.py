import qrcode


def generate_qr(url, filename="qrcode.png"):
    # 创建二维码对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # 添加数据
    qr.add_data(url)
    qr.make(fit=True)

    # 生成图片
    img = qr.make_image(fill_color="black", back_color="white")

    # 保存图片
    img.save(filename)
    print(f"二维码已生成并保存为 {filename}")


# 在这里替换您的链接
target_url = "https://mddfiles.oss-cn-shanghai.aliyuncs.com/mdd-back-all/.upload/2025/11/20/b0986fd4-b7e8-44b0-a475-fb07c602b858.jpeg"
generate_qr(target_url)