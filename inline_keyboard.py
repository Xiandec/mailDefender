from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import methods


BTN_GET_BACK= InlineKeyboardButton('Назад на странцу 1', callback_data='page1')

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

        LEFT_ARROW = InlineKeyboardButton(str(max(1, page - 1)) + ' <',
                                           callback_data='page' + str(max(1, page - 1)))
        RIGHT_ARROW = InlineKeyboardButton('> ' + str(min((letters_num // paginate_by), page + 1)),
                                            callback_data='page' + str(min((letters_num // paginate_by), page + 1)))
        BTN_PAGE = InlineKeyboardButton(' - ' + str(page) + '/' + str(letters_num // paginate_by) + ' - ', callback_data='no_move')
        
        keyboard.add(LEFT_ARROW, BTN_PAGE, RIGHT_ARROW)
        if page != 1:
            keyboard.add(BTN_GET_BACK)
    else:
        keyboard = GET_BACK
    return keyboard