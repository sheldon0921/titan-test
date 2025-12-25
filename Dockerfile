# 使用官方轻量级 Python 镜像 (完美支持 M1 ARM 架构)
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# --- 新增这一行 ---
# 将 /app 加入到 Python 的搜索路径中
ENV PYTHONPATH=/app
# ----------------

# 先复制依赖文件 (利用 Docker 缓存机制，加速构建)
COPY requirements.txt .

# 安装依赖
# --no-cache-dir 可以减小镜像体积
# 使用清华源加速
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制当前目录下的所有代码到容器里
COPY . .

# 默认运行命令：运行 pytest，-v 显示详细信息，-s 允许控制台输出 print 内容
CMD ["pytest", "-v", "-s"]