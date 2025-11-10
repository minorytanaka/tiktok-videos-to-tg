import asyncio
import logging
import os
import time
from urllib.parse import urlencode

import aiofiles
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from bs4 import BeautifulSoup

from settings import allowed_ids, bot_token, chat_id, ip, port

DELETE_VIDEO_DELAY = 3

logging.basicConfig(level=logging.INFO)
local_server = TelegramAPIServer.from_base(f"http://{ip}:{port}")
session = AiohttpSession(api=local_server)
bot = Bot(token=bot_token, session=session)
dp = Dispatcher()

logger = logging.getLogger(__name__)

async def main():
    await dp.start_polling(bot)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Отправь мне ссылку на тик-ток видео")


@dp.message(F.text.regexp(r"http://|https://") | F.text.regexp(r"tiktok|douyin"))
async def upload_to_channel(message: types.Message):
    user_id = message.from_user.id
    user_chat_id = message.chat.id

    if user_id not in allowed_ids:
        print(f"❌ Отказано: {user_id=}")
        await message.answer("Недостаточно прав ❌")
        return

    current_message = await bot.send_message(
        chat_id=message.chat.id, text="Получил ссылку, загружаю в сервис"
    )

    # Build and request
    body = urlencode({"q": message.text, "lang": "ru"})
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url="https://snaptik.net/api/ajaxSearch",
            data=body,
            headers={
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36",
            },
        ) as response:
            response = await response.json()

    # Check status code
    if response["status"] != "ok":
        await current_message.edit_text(
            text="Статус код не 'ok'",
            disable_web_page_preview=False,
        )

    # Parsing link video
    soup = BeautifulSoup(response["data"], "html.parser")
    video_url = "".join(
        link.get("href")
        for link in soup.find_all("a", class_="tik-button-dl")
        if "HD" in link.get_text(strip=True)
    )
    await current_message.edit_text(
        text="Нашел ссылку на видео, пробую скачать",
        disable_web_page_preview=False,
    )

    try:
        # Downloading Video
        async with aiohttp.ClientSession() as session:
            async with session.get(
                video_url, timeout=aiohttp.ClientTimeout(total=30000)
            ) as response:
                response.raise_for_status()
                file_name = f"{int(time.time())}.mp4"
                downloaded = 0
                chunk_size = 1048576  # 1 MB
                async with aiofiles.open(file_name, "wb") as file:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        if chunk:
                            await file.write(chunk)
                            downloaded += len(chunk)

        await current_message.edit_text(
            text="Видео скачано, отправляю...",
            disable_web_page_preview=False,
        )
        await bot.send_video(
            chat_id=user_chat_id,
            video=FSInputFile(file_name),
            supports_streaming=True,
            request_timeout=300,
        )
    except Exception as e:
        print("ERR_DOWNLOADING", e)
        await current_message.edit_text(
            text=f"Ошибка: {e}",
            disable_web_page_preview=False,
        )
    finally:    
        try:
            await asyncio.sleep(DELETE_VIDEO_DELAY)
            os.remove(file_name)
        except Exception as e:
            print("ERR_DELETE", e)


if __name__ == "__main__":
    asyncio.run(main())
