import asyncio
import logging
import os
import time
from urllib.parse import urlencode

import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from bs4 import BeautifulSoup

from settings import admin_id, bot_token, chat_id


logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, отправь ссылку на видео из TikTok")


@dp.message(F.text.regexp(r"http://|https://") | F.text.regexp(r"tiktok|douyin"))
async def video_download(message: types.Message):
    if message.from_user.id != admin_id:
        await message.answer("You are not admin.")
        return

    current_message = await bot.send_message(
        chat_id=message.chat.id, text="Downloading..."
    )

    # Build and request
    body = urlencode({"q": message.text, "lang": "ru"})
    response = requests.post(
        url="https://snaptik.net/api/ajaxSearch",
        data=body,
        headers={
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36",
        },
    ).json()

    # Check status code
    if response["status"] != "ok":
        await current_message.edit_text(
            chat_id=message.chat.id,
            message_id=current_message.message_id,
            text="Status code not ok",
            disable_web_page_preview=False,
        )

    # Parsing link video
    soup = BeautifulSoup(response["data"], "html.parser")
    video_url = "".join(
        link.get("href")
        for link in soup.find_all("a", class_="tik-button-dl")
        if "HD" in link.get_text(strip=True)
    )

    # Downloading Video
    with requests.get(video_url, timeout=(50, 10000), stream=True) as response:
        response.raise_for_status()
        file_name = f"{int(time.time())}.mp4"
        downloaded = 0
        chunk_size = 1048576  # 1 MB
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)

    await bot.send_video(chat_id=chat_id, video=FSInputFile(file_name), supports_streaming=True)
    await current_message.edit_text("Video uploaded to Telegram!🥳")

    try:
        os.remove(file_name)
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id, text="Error deleting file: " + str(e)
        )


if __name__ == "__main__":
    asyncio.run(main())
