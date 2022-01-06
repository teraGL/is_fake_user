import os
import telebot
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)
db_users = os.getenv('USERS').split(',')
logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {message}")

def showUserID(chat_id, user_id):
    bot.send_message(chat_id, user_id)

def id_logger(user_id, status_msg):
    logger.info(f"ID: {user_id}, STATUS: {status_msg}")

@bot.message_handler(content_types=['text'])
def verify(message):
    SUCCESS_MSG = "✅ OK - SECURE ✅"
    FAIL_MSG    = "🆘 USER NOT FOUND 🆘"
    WARNING_MSG = "⚠️ This user hid his account information in Telegram's privacy settings, so I can't tell you anything about him. ⚠️"

    if not message.forward_from:
        bot.send_message(message.chat.id, WARNING_MSG)
        id_logger("HIDDEN", "WARNING")
    else:
        user_id = str(message.forward_from.id)
        # showUserID(message.chat.id, user_id)
        if user_id in db_users:
            bot.send_message(message.chat.id, SUCCESS_MSG)
            id_logger(user_id, "SUCCESS")
        else:
            bot.send_message(message.chat.id, FAIL_MSG)
            id_logger(user_id, "FAIL")

bot.polling()
