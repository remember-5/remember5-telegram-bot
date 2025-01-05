import os
import asyncio
import aiohttp
from telegram import Bot

async def download_file_chunk(session, url, start, end, file_path):
    """
    下载文件的指定部分。
    """
    headers = {"Range": f"bytes={start}-{end}"}
    async with session.get(url, headers=headers) as response:
        with open(file_path, "rb+") as f:
            f.seek(start)
            f.write(await response.read())

async def download_large_file(file_id: str, file_path: str, bot: Bot):
    """
    使用多线程下载大文件（如视频）。
    """
    # 检查文件是否已存在
    if os.path.exists(file_path):
        print(f"文件已存在，跳过下载: {file_path}")
        return

    # 获取文件下载链接
    file = await bot.get_file(file_id)
    file_url = file.file_path

    # 获取文件大小
    async with aiohttp.ClientSession() as session:
        async with session.head(file_url) as response:
            file_size = int(response.headers["Content-Length"])

    # 分块下载
    chunk_size = 1024 * 1024 * 5  # 每个块 5MB
    chunks = range(0, file_size, chunk_size)

    # 创建空文件
    with open(file_path, "wb") as f:
        f.truncate(file_size)

    # 多线程下载
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_file_chunk(session, file_url, start, start + chunk_size - 1, file_path)
            for start in chunks
        ]
        await asyncio.gather(*tasks)

async def download_small_file(file_id: str, file_path: str, bot: Bot):
    """
    直接下载小文件（如图片）。
    """
    # 检查文件是否已存在
    if os.path.exists(file_path):
        print(f"文件已存在，跳过下载: {file_path}")
        return

    # 下载文件
    file = await bot.get_file(file_id)
    await file.download_to_drive(file_path)
