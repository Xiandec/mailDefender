import logging
import random
import string
import yaml
import os
import json



from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import inline_keyboard
import messages
import methods
from config import Config

logging.basicConfig(level=logging.INFO)

conf = Config()
bot = Bot(conf.get_value('bot_token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# start reg to bot
@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    await message.answer(
            text=messages.start_page(),
            reply_markup=inline_keyboard.get_letters_by_page()
        )

@dp.message_handler() # Он принимает все запросы без фильтров
async def start(message: types.Message):
    await message.answer(
            text=messages.error_msg()
        )
    await message.answer(
            text=messages.start_page(),
            reply_markup=inline_keyboard.get_letters_by_page()
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
