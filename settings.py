from environs import Env

env = Env()
env.read_env()


bot_token = env.str("BOT_TOKEN")
chat_id = env.int("CHAT_ID")
admin_id = env.int("ADMIN_ID")
ip = env.str("BOT_API_IP")
port = env.str("PORT")
