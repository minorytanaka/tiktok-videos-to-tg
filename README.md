# TikTok Video Downloader Bot

## EN

### Project Description

This project is a Telegram bot written in Python using the **aiogram** library. The bot allows users to download videos from TikTok and send them to a Telegram chat. It accepts a TikTok video link, downloads it, and sends it to a specified chat. This bot is intended for administrators, as access to its features is restricted by user rights.

In order for the bot to work properly, you need to add it to your channel and grant it permission to create posts. This is necessary for the bot to send downloaded videos directly to the channel.

### Features

- **Bot Startup**: The bot starts and listens for user commands.
- **`/start` Command**: When the `/start` command is sent, the bot greets the user and informs them about the possibility of sending a video link.
- **Video Download**: After a TikTok video link is sent, the bot downloads the video and sends it to the chat. The video is downloaded in MP4 format and transmitted via Telegram.
- **Administrator Rights**: The video download function is available only to the bot administrator. Access is checked using the `admin_id`.

### Key Components

- **aiogram**: The bot uses the asynchronous library to interact with the Telegram API.
- **requests**: Used for sending HTTP requests to search for and download videos.
- **BeautifulSoup**: Used for parsing the HTML page and extracting the video link.
- **.env file**: For securely storing and using sensitive data such as the bot token and the administrator's ID.

### Technologies

- **Python 3.12.6**
- **aiogram 3.17.0**
- **BeautifulSoup 4.12.3**
- **requests**


### How to use

1. Use the generator instructions to compile Telegram Bot Api: https://tdlib.github.io/telegram-bot-api/build.html.
2. Start the Telegram Bot Api server:
```bash
telegram-bot-api --local --api-id=<api_id> --api-hash=<api_hash>
```
3. Transfer bot to Local Bot API
To switch your bot to a local api server, you first need to disconnect it from the Telegram Bot Api cloud platform.
There is a logOut method for this purpose. You can simply open the link in your browser by replacing <BOT_TOKEN> with your bot's real token:
``bash
https://api.telegram.org/bot<BOT_TOKEN>/logOut
```
4. If no errors appear and the server has taken over the terminal, then all is well. To make sure, open another terminal and run the command:
```bash
curl http://<ip_address_telegram_bot_api>:8081
```
In response, you should see the following:
{“ok”:false, “error_code”:404, “description”: “Not Found”}.
5. Clone the repository:
```bash
git clone https://github.com/minorytanaka/tiktok-videos-to-tg.git
cd tiktok-videos-to-tg
```
6. Create an `.env` file and add your variables:
```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_user_id
CHAT_ID=your_chat_id
```
7. Build and run the project using Docker Compose:
```bash
docker-compose up --build
```
8. The bot will now be up and available. Send the link to the TikTok video to the bot and it will download and send the video to your chat.

---

## RU

### Описание проекта

Этот проект представляет собой Telegram-бота, написанного на Python с использованием библиотеки **aiogram**. Бот позволяет загружать видео с TikTok и отправлять их в чат Telegram. Он принимает ссылку на видео из TikTok, скачивает его и отправляет в заданный чат. Этот бот предназначен для администраторов, так как доступ к функционалу ограничен правами пользователя.

Для корректной работы бота необходимо добавить его в ваш канал и предоставить ему права на создание постов. Это необходимо для того, чтобы бот мог отправлять загруженные видео непосредственно в канал.

### Функции

- **Запуск бота**: Бот начинает свою работу и слушает команды пользователей.
- **Команда `/start`**: При отправке команды `/start` бот приветствует пользователя и сообщает о возможности отправки ссылки на видео.
- **Скачивание видео**: После отправки ссылки на видео из TikTok бот скачивает его и отправляет в чат. Видео загружается в формате MP4 и передается через Telegram.
- **Права администратора**: Функция скачивания видео доступна только администратору бота, проверка осуществляется по `admin_id`.

### Основные компоненты

- **aiogram**: Бот использует асинхронную библиотеку для работы с Telegram API.
- **requests**: Для отправки HTTP-запросов для поиска и скачивания видео.
- **BeautifulSoup**: Для парсинга HTML-страницы и извлечения ссылки на видео.
- **.env файл**: Для безопасного хранения и использования конфиденциальных данных, таких как токен бота и ID администратора.

### Технологии

- **Python 3.12.6**
- **aiogram 3.17.0**
- **BeautifulSoup 4.12.3**
- **requests**



### Как использовать

1. Воспользуйтесь генератором инструкция для компиляции Telegram Bot Api: https://tdlib.github.io/telegram-bot-api/build.html
2. Запускаем сервер Telegram Bot Api:
```bash
telegram-bot-api --local --api-id=<api_id> --api-hash=<api_hash>
```
3. Перенос бота на Local Bot API
Чтобы переключить вашего бота на локальный сервер api, сначала нужно отключить его от облачной платформы Telegram Bot Api.
Для этого существует метод logOut. Вы можете просто открыть в браузере ссылку, заменив <BOT_TOKEN> на настоящий токен вашего бота:
```bash
https://api.telegram.org/bot<BOT_TOKEN>/logOut
```
4. Если никаких ошибок не появилось и сервер занял собой терминал, значит все хорошо. Чтобы окончательно убедиться, откройте еще один терминал и выполните команду:
```bash
curl http://<айпи_адрес_где_запущен_телеграм_бот_апи>:8081
```
В ответ вы должны увидеть следующее:
{"ok":false,"error_code":404,"description":"Not Found"}
5. Клонируйте репозиторий:
```bash
git clone https://github.com/minorytanaka/tiktok-videos-to-tg.git
cd tiktok-videos-to-tg
```
6. Создайте файл `.env` и добавьте свои переменные:
```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_user_id
CHAT_ID=your_chat_id
```
7. Соберите и запустите проект с использованием Docker Compose:
```bash
docker-compose up --build
```
8. Теперь бот будет запущен и доступен. Отправьте ссылку на видео TikTok боту, и он скачает и отправит видео в ваш чат.
