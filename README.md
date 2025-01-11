
Вот обновленная инструкция с добавлением блока информации о добавлении сервисного файла для автоматического запуска:

---

## EN

### Project Description

This project is a Telegram bot written in Python using the **aiogram** library. The bot is designed to download videos from TikTok and send them to a specified Telegram chat. To use its functionality, authorization is required: access is granted only to the user with the ID specified in the `.env` file (variable `ADMIN_ID`).  
The video is deleted from the server after being sent to the chat.

For the bot to function correctly, it must be added to your channel and granted posting permissions.

### Features

- **Command `/start`**: The bot greets the user and provides instructions for sending video links.
- **Video Downloading**: The bot accepts a TikTok video link, downloads it in MP4 format, and sends it to the specified chat.
- **Access Restriction**: Only the bot administrator, identified by the `ADMIN_ID` variable, has access to its functionality.

### Key Components

- **aiogram**: An asynchronous library for working with the Telegram API.
- **requests**: Used to perform HTTP requests for fetching and downloading videos.
- **BeautifulSoup**: Used to parse HTML pages and extract video links.
- **.env file**: Securely stores sensitive data such as the bot token and administrator ID.

### Technologies

- **Python 3.12.6**
- **aiogram 3.17.0**
- **BeautifulSoup 4.12.3**
- **requests**

### How to Use

1. **Set up the Local Bot API**:
    
    - Follow the [compilation guide](https://tdlib.github.io/telegram-bot-api/build.html) to configure the Local Telegram Bot API.
2. **Start the Local Bot API**:
    
    ```bash
    telegram-bot-api --local --api-id=<api_id> --api-hash=<api_hash>
    ```
    
3. **Switch the Bot to the Local Bot API**:
    
    - Use the `logOut` method to disconnect the bot from the cloud-based Telegram Bot API:
    
    ```bash
    https://api.telegram.org/bot<BOT_TOKEN>/logOut
    ```
    
4. **Verify the Server**:
    
    - If the server starts successfully, run the following command:
    
    ```bash
    curl http://<server_ip_address>:8081
    ```
    
    - Expected response: `{"ok":false,"error_code":404,"description":"Not Found"}`.
5. **Clone the Repository**:
    
    ```bash
    git clone https://github.com/minorytanaka/tiktok-videos-to-tg.git
    cd tiktok-videos-to-tg
    ```
    
6. **Create a `.env` File**:  
    Add your parameters to the `.env` file:
    
    ```env
    BOT_TOKEN=your_telegram_bot_token
    ADMIN_ID=your_user_id
    CHAT_ID=your_chat_id
    ```
    
7. **Run the Bot Using Docker Compose**:
    
    ```bash
    docker compose up
    ```
    
8. **Usage**:
    
    - Send a TikTok video link to the bot.
    - The bot will download the video and send it to your chat.

### Optional: Create a service for autorun Local Bot API

If you'd like the bot to start automatically when your system boots, you can create a `systemd` service. Here's how to do it.
If another instance of Telegram Bot API is already running, there may be a conflict. Check if the process is active: `ps aux | grep telegram-bot-api` and terminate `kill <id>` or `kill -9 <id>` (forced termination).

1. **Create the Service File**:
    
    Create a new file for the service:
    
    ```bash
    sudo nano /etc/systemd/system/telegram-bot-api.service
    ```
    
    Paste the following content into the file, adjusting the paths as necessary:
    
    ```ini
    [Unit]
    Description=Telegram Bot API Server
    After=network.target
    
    [Service]
    ExecStart=/root/telegram-bot-api/build/telegram-bot-api --local --api-id=<api_id> --api-hash=<api_hash>
    WorkingDirectory=/root/telegram-bot-api/build
    Restart=always
    User=root
    Group=root
    
    [Install]
    WantedBy=multi-user.target
    ```
    
2. **Reload Systemd**:
    
    Run the following command to reload systemd and apply the new service configuration:
    
    ```bash
    sudo systemctl daemon-reload
    ```
    
3. **Enable the Service**:
    
    Enable the service to start automatically on boot:
    
    ```bash
    sudo systemctl enable telegram-bot-api.service
    ```
    
4. **Start the Service**:
    
    Start the service manually for the first time:
    
    ```bash
    sudo systemctl start telegram-bot-api.service
    ```
    
5. **Check the Status**:
    
    Check if the service is running correctly:
    
    ```bash
    sudo systemctl status telegram-bot-api.service
    ```
## RU

### Описание проекта

Проект представляет собой Telegram-бота, написанного на Python с использованием библиотеки **aiogram**. Бот предназначен для скачивания видео с TikTok и отправки их в указанный чат Telegram. Для использования функционала требуется авторизация: доступ имеет только пользователь с ID, указанным в файле `.env` (переменная `ADMIN_ID`). Видео удаляется с сервера после отправки в чат.

Для корректной работы бота его необходимо добавить в ваш канал и предоставить права на создание сообщений.

### Функции

- **Команда `/start`**: Бот приветствует пользователя и предоставляет инструкции по отправке ссылок на видео.
- **Скачивание видео**: Бот принимает ссылку на видео TikTok, загружает его в формате MP4 и отправляет в заданный чат.
- **Ограничение доступа**: Доступ к функционалу имеет только администратор, чей ID проверяется через переменную `ADMIN_ID`.

### Основные компоненты

- **aiogram**: Асинхронная библиотека для работы с Telegram API.
- **requests**: Для выполнения HTTP-запросов для поиска и скачивания видео.
- **BeautifulSoup**: Для парсинга HTML-страниц и извлечения ссылок на видео.
- **.env файл**: Для безопасного хранения конфиденциальных данных, таких как токен бота и ID администратора.

### Технологии

- **Python 3.12.6**
- **aiogram 3.17.0**
- **BeautifulSoup 4.12.3**
- **requests**

### Как использовать

1. **Настройка Local Bot API**:
    
    - Для запуска локального API Telegram Bot следуйте [инструкции по компиляции](https://tdlib.github.io/telegram-bot-api/build.html).
2. **Запуск Local Bot API**:
    
    ```bash
    telegram-bot-api --local --api-id=<api_id> --api-hash=<api_hash>
    ```
    
3. **Переключение бота на Local Bot API**:
    
    - Используйте метод `logOut` для отключения бота от облачной Telegram Bot API:
    
    ```bash
    https://api.telegram.org/bot<BOT_TOKEN>/logOut
    ```
    
4. **Проверка работы сервера**:
    
    - Если сервер успешно запущен, выполните команду:
    
    ```bash
    curl http://<айпи_адрес_сервера>:8081
    ```
    
    - Ожидаемый ответ: `{"ok":false,"error_code":404,"description":"Not Found"}`.
5. **Клонирование репозитория**:
    
    ```bash
    git clone https://github.com/minorytanaka/tiktok-videos-to-tg.git
    cd tiktok-videos-to-tg
    ```
    
6. **Создание файла `.env`**: Добавьте в файл `.env` ваши параметры:
    
    ```env
    BOT_TOKEN=your_telegram_bot_token
    ADMIN_ID=your_user_id
    CHAT_ID=your_chat_id
    ```
    
7. **Запуск через Docker Compose**:
    
    ```bash
    docker compose up
    ```
    
8. **Использование**:
    
    - Отправьте боту ссылку на видео TikTok.
    - Бот загрузит видео и отправит его в ваш чат.

### Опционально: Создаем сервис для автозапуска Local Bot API

Если вы хотите, чтобы Local Bot API запускался автоматически при старте системы, можно создать сервисный файл `systemd`.
Если уже запущен другой экземпляр Telegram Bot API, может быть конфликт. Проверьте, активен ли процесс: `ps aux | grep telegram-bot-api` и завершите процесс `kill <id>` либо `kill -9 <id>` (принудительное завершение).

1. **Создайте сервисный файл**:
    
    Создайте новый файл для сервиса:
    
    ```bash
    sudo nano /etc/systemd/system/telegram-bot-api.service
    ```
    
    Вставьте следующий контент в файл, заменив пути при необходимости:
    
    ```ini
    [Unit]
    Description=Telegram Bot API Server
    After=network.target
    
    [Service]
    ExecStart=/root/telegram-bot-api/build/telegram-bot-api --local --api-id=<api_id> --api-hash=<api_hash>
    WorkingDirectory=/root/telegram-bot-api/build
    Restart=always
    User=root
    Group=root
    
    [Install]
    WantedBy=multi-user.target
    ```
    
2. **Перезагрузите systemd**:
    
    Выполните команду для перезагрузки systemd и применения новой конфигурации сервиса:
    
    ```bash
    sudo systemctl daemon-reload
    ```
    
3. **Включите сервис**:
    
    Включите сервис для автоматического старта при загрузке системы:
    
    ```bash
    sudo systemctl enable telegram-bot-api.service
    ```
    
4. **Запустите сервис**:
    
    Запустите сервис вручную в первый раз:
    

	```bash
	sudo systemctl start telegram-bot-api.service
	```

5. **Проверьте статус**:
    
    Проверьте, что сервис работает правильно:
    
    ```bash
    sudo systemctl status telegram-bot-api.service
    ```
---
