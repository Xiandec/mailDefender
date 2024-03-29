"""
Модуль бота
"""

import requests
import logging
import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re

from config import Config


conf = Config()

def from_subj_decode(msg_from_subj) -> str:
    """
    Функция декодирует строку письма, если та закодированна
    """
    if msg_from_subj:
        encoding = decode_header(msg_from_subj)[0][1]
        msg_from_subj = decode_header(msg_from_subj)[0][0]
        if isinstance(msg_from_subj, bytes):
            msg_from_subj = msg_from_subj.decode(encoding)
        if isinstance(msg_from_subj, str):
            pass
        msg_from_subj = str(msg_from_subj).strip("<>").replace("<", "")
        return msg_from_subj
    else:
        return

def get_all_uid_letters() -> list:
    """
    Функция возвращает все `uid` писем на почте
    """
    mail_pass = conf.get_value('mail_pass')
    username = conf.get_value('username')
    imap_server = conf.get_value('imap_server')
    try:
        with imaplib.IMAP4_SSL(imap_server) as imap:
            imap.login(username, mail_pass)
            imap.select("INBOX")
            status, id = imap.uid('search', 'ALL')
            if status == 'OK':
                return id[0].decode("utf-8").split(' ')
    except ConnectionRefusedError:
        logging.error("ConnectionRefusedError: [Errno 61] Connection refused")
    except BaseException:
        logging.error("BaseException")
    return
    
def get_letters_by_page(
        page: int = 1,
        paginate_by : int = 10
        ) -> dict:
    """
    Функция возвращает письма на странице (пагинация)
    """
    mail_pass = conf.get_value('mail_pass')
    username = conf.get_value('username')
    imap_server = conf.get_value('imap_server')
    try:
        response = {}

        with imaplib.IMAP4_SSL(imap_server) as imap:
            imap.login(username, mail_pass)
            imap.select("INBOX")
            status, id = imap.uid('search', 'ALL')
            if status == 'OK':
                uids = id[0].decode("utf-8").split(' ')
                uids.reverse()
                for uid in uids[(page - 1) * paginate_by:page * paginate_by]:
                    status, msg = imap.uid('fetch', uid.encode("utf-8"), '(RFC822)')
                    if status == 'OK':
                        msg = email.message_from_bytes(msg[0][1])
                        if msg["Subject"]:
                            header = from_subj_decode(msg["Subject"])
                        else:
                            header = 'Пустая тема'
                        response[str(uid)] = header + ' ' + msg['Return-path']
                return response
    except ConnectionRefusedError:
        logging.error("ConnectionRefusedError: [Errno 61] Connection refused")
    except BaseException:
        logging.error("BaseException")
    return

def get_letter_by_uid(uid : str) -> dict:
    """
    Функция возвращает письмо по его `uid`

    В словаре записываются следующие значения: 

    - `header` - заголовок письма, или 'пустая тема'
    - `text` - текст письма, если есть
    - `html` - html код письма, если есть
    - `attachment` - все вложения письма, если нет, то пустой список
    """
    mail_pass = conf.get_value('mail_pass')
    username = conf.get_value('username')
    imap_server = conf.get_value('imap_server')
    try:
        response = {'attachment' : []}
        with imaplib.IMAP4_SSL(imap_server) as imap:
            imap.login(username, mail_pass)
            imap.select("INBOX")
            status, msg = imap.uid('fetch', uid.encode("utf-8"), '(RFC822)')
            if status == 'OK':
                msg = email.message_from_bytes(msg[0][1])
                if msg["Subject"]:
                    header = from_subj_decode(msg["Subject"])
                else:
                    header = 'Пустая тема'
                response['header'] = header
                for part in msg.walk():
                    try:
                        if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                            response['text'] = base64.b64decode(part.get_payload()).decode()

                        if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'html':
                            response['html'] = base64.b64decode(part.get_payload()).decode().replace('<HTML>', '<HTML><meta charset="UTF-8">')
                                
                        if part.get_content_disposition() == 'attachment':
                            filename = from_subj_decode(part.get_filename())
                            response['attachment'].append({'filename': filename, 'file': part.get_payload(decode=True)})
                    except BaseException:
                        pass
                return response
    except ConnectionRefusedError:
        logging.error("ConnectionRefusedError: [Errno 61] Connection refused")
    except BaseException:
        logging.error("BaseException")
    return

if __name__ == '__main__':
    print(len(list(get_letters_by_page(2).keys())))