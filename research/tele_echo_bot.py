import logging
from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_API_TOKEN)
dispatcher = Dispatcher(bot=bot)

@dispatcher.message_handler(commands=['start', 'help'])
async def command_start_handler(message:types.Message):
    """
    This handler receives message with 'start' or 'help' command.
    """
    await message.reply("Hi")

@dispatcher.message_handler()
async def echo(msg:types.Message):
    """ 
    This will return the same message
    """
    await msg.answer(msg.text)

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)