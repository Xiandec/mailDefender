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

def get_all_uid_letters():
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
        ):
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
                            header = decode_header(msg["Subject"])[0][0]
                            header = (header.decode() if isinstance(header, bytes) else header)
                        else:
                            header = 'Пустая тема'
                        response[str(uid)] = header + ' ' + msg['Return-path']
                return response
    except ConnectionRefusedError:
        logging.error("ConnectionRefusedError: [Errno 61] Connection refused")
    except BaseException:
        logging.error("BaseException")
    return

if __name__ == '__main__':
    print(len(list(get_letters_by_page(2).keys())))