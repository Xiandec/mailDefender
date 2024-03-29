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
    """
    Стартовое сообщение для бота, отправляет первую страницу писем
    """

    await message.answer(
            text=messages.start_page(),
            reply_markup=inline_keyboard.get_letters_by_page()
        )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('letter'))
async def process_callback_letter(callback_query: types.CallbackQuery):
    """
    Отправляет всё что есть в письме по нажатию на кнопку письма
    """
    code = callback_query.data.replace('letter', '')
    if code.isdigit():
        code = str(code)
    # get letter
    letter = methods.get_letter_by_uid(code)
    if letter: # if letter isnt None

        if 'text' in letter: # if text 
            if len(letter['text']) > 4096: # if text too long
                await bot.edit_message_text(
                    chat_id=callback_query.from_user.id,
                    text=letter['header'] + '\n' + 'Текст слишком длинный для телеграм',
                    message_id=callback_query.message.message_id
                    )
            else: # if text nit long
                await bot.edit_message_text(
                chat_id=callback_query.from_user.id,
                text=letter['header'] + '\n' + letter['text'],
                message_id=callback_query.message.message_id
                )

        elif 'text' not in letter: # send only `header`
            await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            text=letter['header'],
            message_id=callback_query.message.message_id
            )

        if 'html' in letter: # send `html` code of letter
            await bot.send_document(
                chat_id=callback_query.from_user.id,
                document=('letter.html', letter['html'])
            )

        if len(letter['attachment']) > 0: # if any attachments
            for attachment in letter['attachment']:
                await bot.send_document(
                    chat_id=callback_query.from_user.id,
                    document=(attachment['filename'], attachment['file'])
                )

    await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=messages.start_page(),
            reply_markup=inline_keyboard.get_letters_by_page()
        )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('page'))
async def process_callback_letters_page(callback_query: types.CallbackQuery):
    """
    Отправляет новую странцу писем
    """
    code = callback_query.data.replace('page', '')
    if code.isdigit():
        code = int(code)
    
    await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=messages.start_page(),
            reply_markup=inline_keyboard.get_letters_by_page(page=code)
        )

@dp.message_handler() # Он принимает все запросы без фильтров
async def error(message: types.Message):
    await message.answer(
            text=messages.error_msg()
        )
    await message.answer(
            text=messages.start_page(),
            reply_markup=inline_keyboard.get_letters_by_page()
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
