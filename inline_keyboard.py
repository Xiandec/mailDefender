from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import methods
import json


BTN_GET_BACK= InlineKeyboardButton('Назад', callback_data='get_back')

GET_BACK = InlineKeyboardMarkup().add(BTN_GET_BACK)

def get_letters_by_page(
        page: int = 1,
        paginate_by : int = 10
        ):
    """
    Функция для создания клавиатуры навигации по письмам
    """
    letters = methods.get_letters_by_page(page=page, paginate_by=paginate_by)
    letters_num = len(methods.get_all_uid_letters())
    if letters and letters_num:
        keyboard = InlineKeyboardMarkup()
        for key, value in letters.items():
            BTN_1 = InlineKeyboardButton(value, callback_data='letter' + str(key))
            keyboard.add(BTN_1)

        LEFT_ARROW = InlineKeyboardButton('<', callback_data='<' + str(max(0, page - 1)))
        RIGHT_ARROW = InlineKeyboardButton('>', callback_data='>' + str(min((letters_num // paginate_by), page + 1)))
        
        keyboard.add(LEFT_ARROW, BTN_GET_BACK, RIGHT_ARROW)
    else:
        keyboard = GET_BACK
    return keyboard