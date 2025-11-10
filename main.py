import asyncio
import logging
import os
import time
from urllib.parse import urlencode
from db_handler import DBService

import aiofiles
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bs4 import BeautifulSoup

from settings import allowed_ids, bot_token, chat_id_to_send, ip, port

DELETE_VIDEO_DELAY = 3

local_server = TelegramAPIServer.from_base(f"http://{ip}:{port}")
session = AiohttpSession(api=local_server)
bot = Bot(token=bot_token, session=session)
dp = Dispatcher()

logger = logging.getLogger(__name__)
db = DBService()


async def main():
    await dp.start_polling(bot)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Отправка в канал", callback_data="set_mode_CHANNEL")],
            [InlineKeyboardButton(text="💬 Отправка пользователю", callback_data="set_mode_PRIVATE")]
        ]
    )
    await message.answer(
        "Привет 👋\nВыбери режим работы бота:",
        reply_markup=keyboard
    )


@dp.callback_query(F.data.startswith("set_mode_"))
async def set_mode(callback: CallbackQuery):
    mode_value = callback.data.replace("set_mode_", "")
    mode_id = db.get_mode_by_name(mode_value)

    user = callback.from_user
    db.add_user(user.id, user.username, user.first_name, mode_id)

    text = "✅ Режим сохранён: "
    if mode_value == "CHANNEL":
        text += "отправка видео в канал 📢"
    elif mode_value == "PRIVATE":
        text += "отправка только тебе 💬"

    await callback.message.edit_text(text)
    await callback.answer("Режим установлен!")


@dp.message(Command("channel"))
async def cmd_start(message: types.Message):
    mode_id = db.get_mode_by_name("CHANNEL")
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, mode_id)
    await message.answer("Супер, я запомнил)")


@dp.message(Command("private"))
async def cmd_start(message: types.Message):
    mode_id = db.get_mode_by_name("PRIVATE")
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, mode_id)
    await message.answer("Супер, я запомнил)")


@dp.message(F.text.regexp(r"http://|https://") | F.text.regexp(r"tiktok|douyin"))
async def upload_to_channel(message: types.Message):
    user_id = message.from_user.id
    mode_value_by_user_id = db.get_mode_value_by_user(user_id)

    if user_id not in allowed_ids:
        logger.info(f"❌ Отказано: {user_id=}")
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
    try:
        soup = BeautifulSoup(response["data"], "html.parser")
    except KeyError:
        logger.info(f"Не корректная ссылка: {message.text}")
        await message.answer("Не корректная ссылка братанчик, проверь, точно ли рабочая")
        return
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
        chat_id = None
        if mode_value_by_user_id == "PRIVATE":
            chat_id = message.chat.id
        elif mode_value_by_user_id == "CHANNEL":
            chat_id = chat_id_to_send
        await bot.send_video(
            chat_id=chat_id,
            video=FSInputFile(file_name),
            supports_streaming=True,
            request_timeout=300,
        )
    except Exception as e:
        logger.info("ERR_DOWNLOADING", e)
        await current_message.edit_text(
            text=f"Ошибка: {e}",
            disable_web_page_preview=False,
        )
    finally:    
        try:
            await asyncio.sleep(DELETE_VIDEO_DELAY)
            os.remove(file_name)
        except Exception as e:
            logger.info("ERR_DELETE", e)


@dp.message(Command("mode"))
async def cmd_mode(message: types.Message):
    user_id = message.from_user.id
    try:
        current_mode = db.get_mode_value_by_user(user_id)
    except Exception:
        current_mode = None

    if current_mode:
        text = f"⚙️ Текущий режим: <b>{current_mode}</b>\n\nХочешь поменять?"
    else:
        text = "Ты ещё не выбрал режим.\nВыбери, как бот будет отправлять видео:"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Отправка в канал", callback_data="set_mode_CHANNEL")],
        [InlineKeyboardButton(text="💬 Отправка пользователю", callback_data="set_mode_PRIVATE")]
    ])

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


if __name__ == "__main__":
    db.init_db()
    db.add_modes()
    asyncio.run(main())
