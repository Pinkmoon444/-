import os 
import time 
import datetime
import pytz
import pathlib

import requests 
# pip install requests

# pip install python-dotenv
from dotenv import load_dotenv

#pip install python-telegram-bot==13.7
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters

import random 

load_dotenv()
ТОКЕН = os.getenv("токен")

бот = Bot(ТОКЕН)
этот_файл = __file__
эта_папка = pathlib.Path(этот_файл).resolve().parent # функция позволяет узнать родительскую папку


def проверить_входящие(айди=None):
    def создать_last_msg(update_id):
        with open(эта_папка / 'last_msg', 'w', encoding='utf-8') as file:
            file.write(str(update_id))

    def считать_last_msg():
        with open(эта_папка / 'last_msg', 'r', encoding='utf-8') as file:
            return int(file.read())
        
    сейчас = datetime.datetime.now(pytz.UTC)
    if not os.path.exists(эта_папка / 'last_msg'):
        while True:
            try:
                обновления = бот.get_updates()
                if not обновления:
                    time.sleep(0.5)
                    continue
                break
            except:
                continue
        последнее_сообщение = обновления[-1]
        if последнее_сообщение.message.date < сейчас:
            создать_last_msg(последнее_сообщение.update_id)
        else:
            создать_last_msg(последнее_сообщение.update_id - 1)

    while True:
        try:
            обновления = бот.get_updates(offset=считать_last_msg() + 1)
        except:
            time.sleep(1)
            continue
        if not обновления:
            continue

        обновления.reverse()
        print(len(обновления))
        for сообщение in обновления:
            if айди is None or сообщение.effective_user.id == айди:
                создать_last_msg(сообщение.update_id)
                print(сообщение.effective_message.text)
                return сообщение
        time.sleep(0.5)
