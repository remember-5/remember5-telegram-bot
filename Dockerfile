# 使用 Python 3.10 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装 Poetry（使用清华源）
RUN pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目文件
COPY pyproject.toml poetry.lock ./

# 配置 Poetry 使用清华源
RUN poetry config virtualenvs.create false && \
    poetry source add --priority=default tsinghua https://pypi.tuna.tsinghua.edu.cn/simple/

# 安装依赖
RUN poetry install --no-root

# 复制 Bot 代码
COPY . .

# 设置环境变量
ENV TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN

# 运行 Bot
CMD ["poetry", "run", "python", "bot/bot.py"]
