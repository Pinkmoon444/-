import os

# pip install requests
import requests

# pip install python-dotenv
from dotenv import load_dotenv

# pip install python-telegram-bot==13.7
from telegram import Bot 



load_dotenv()
TOKEN = os.getenv("TOKEN")
бот = Bot(TOKEN)
айдишник = 5622354606
бот.send_message(chat_id=айдишник, text = "Бонжур")

def запарсить_погоду():
    ссылка = "https://www.google.com/search"
    параметры = {"q": "погода в коломне"}
    ответ_сайта = requests.get(ссылка, параметры)

    if ответ_сайта.status_code != 200:
        return "Сайт недоступен. Звоните позднее"
    текст = ответ_сайта.text
    
    старт = текст.find("BNeawe iBp4i AP7Wnd")
    if старт == -1:
        return("Первый блок не найден")

    старт = текст.find("°C", старт)
    if старт == -1:
        return "Градусы не найдены."
    старт -= 15
    старт = текст.find(">", старт)
    старт += 1
    стоп = текст.find("<", старт)

    градусы = текст[старт:стоп]

    старт = текст.find("BNeawe tAd8D AP7Wnd", старт)
    if старт == -1:
        return("Второй блок не найден")
    старт = текст.find("\n", старт)
    старт += 1
    стоп = текст.find("<", старт)
    состояние_погоды = текст[старт:стоп]
    return градусы, состояние_погоды