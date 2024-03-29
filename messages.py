from config import Config

conf = Config()

def start_page() -> str:
    msg = f'👋Привет! Вот письма с почты %s:😊' % (conf.get_value('username'), )
    return msg

def error_msg() -> str:
    msg = 'Прости, я не понял😓'
    return msg
