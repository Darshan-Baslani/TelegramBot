import logging
from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv
import openai
import sys

import openai.error 

class Reference:
    """ 
    A class to store previously generated response from openai api
    """
    def __init__(self) -> None:
        self.response = ""


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

reference = Reference()

MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot)

def clear_past():
    """ 
    Clears all the past context and conversation
    """
    reference.response = ""
    
@dispatcher.message_handler(commands=['start'])
async def welcome(message:types.Message):
    """ 
    Receives message with /start command
    """
    await message.reply("Hi\nTell me how can I assist you today?")

@dispatcher.message_handler(commands=['clear'])
async def clear(message:types.Message):
    """ 
    Clears previous conversation and messages.
    """
    clear_past()
    await message.reply("I've cleared past conversation")

@dispatcher.message_handler()
async def chatgpt(message:types.Message):
    """ 
    Processes normal input and output's using openai api
    """
    try:
        print(f">>>USER: \n\t{message.text}")
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages = [
                {"role":"assistant", "content":reference.response},
                {"role":"user", "content":message.text}
            ]
        )
        reference.response = response.choices[0].message["content"]
        print(f">>>ChatGPT: \n\t{reference.response}")
        await bot.send_message(chat_id=message.chat.id, text=reference.response)
    except openai.error.RateLimitError:
        print("OpenAI api's rate limit exceeded")
        await bot.send_message(chat_id=message.chat.id, text="I'm currently overloaded. Please try again later.")

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=False)