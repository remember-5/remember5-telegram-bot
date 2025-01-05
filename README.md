# Introduction
telegram bot

转发消息给bot,实现下载并上传到云盘

# Usage

在项目根目录下运行以下命令，初始化 Alembic：

`poetry run alembic init migrations`

然后，编辑 `alembic.ini` 文件，更新数据库连接字符串：

`sqlalchemy.url = sqlite:///bot.db`
编辑 `migrations/env.py`，配置 `SQLAlchemy` 模型：

```python
from bot.database import Base
from bot.models.user import User  # 导入你的模型

target_metadata = Base.metadata
```

创建迁移脚本
每次修改模型后，运行以下命令生成迁移脚本：

`poetry run alembic revision --autogenerate -m "add_user_table"`
应用迁移：

`poetry run alembic upgrade head`


# Reference

- [tg-auto-install-bot](https://github.com/ershiyi21/myprogram)
- [tgtogd](https://github.com/Xiefengshang/tgtogd)
- [telegram_media_downloader](https://github.com/tangyoha/telegram_media_downloader) 基于Dineshkarthik的项目， 电报视频下载，电报资源下载，跨平台，支持web查看下载进度 ，支持bot下发指令下载，支持下载已经加入的私有群但是限制下载的资源， telegram media download,Download media files from a telegram conversation/chat/channel up to 2GiB per file 
