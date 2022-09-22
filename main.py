import telebot
import requests
from bs4 import BeautifulSoup
import time
from random import choice
import speech_recognition as sr
import os
import uuid
from jokes import get_jokes
from currency import get_dollar, get_euro, get_ruble

chill_phrasess = ['Зачилься браток! Заслужил', 'Ты чертова машина! Остановись, иначе уничтожишь планету своей продуктивностью',
                  'Пацаны не гоните!\n\nВы матерям нужны!']

url = 'https://yandex.kz/pogoda/karaganda/details?via=mf#28'
response = requests.get(url)
bs = BeautifulSoup(response.text, 'lxml')

whats_day = bs.find('span', class_='a11y-hidden')
table_temp_ = bs.find_all('div', class_='weather-table__temp')
temp_value_ = bs.find_all('span', class_='temp__value temp__value_with-unit')

morning = f"Утром температура от {table_temp_[0].text.replace('…',' до ')}, ощущается как {temp_value_[0].text}"
day = f"Днем температура от  {table_temp_[1].text.replace('…',' до ')}, ощущается как {temp_value_[1].text}"
evening = f"Вечером температура от {table_temp_[2].text.replace('…',' до ')}, ощущается как {temp_value_[2].text}"
night = f"Ночью температура от {table_temp_[3].text.replace('…',' до ')}, ощущается как {temp_value_[3].text}"

language='ru_RU'
r = sr.Recognizer()

print("Работаем")

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

def currency_rate(message):
    bot.send_message(message.from_user.id, "Курс валют чееееек")
    bot.send_message(message.from_user.id, "Курс Доллара " + get_dollar()+'💲')
    bot.send_message(message.from_user.id, "Курс Евро " + get_euro()+'💶')
    bot.send_message(message.from_user.id, "Курс Рубля " + get_ruble()+'💴')
def weather_report(message):
    bot.send_message(message.from_user.id, "Прогноз погоды чееееек")
    bot.send_message(message.from_user.id, f"{whats_day.text.replace(',', '').capitalize()}")
    bot.send_message(message.from_user.id, f"🌞{morning}")
    bot.send_message(message.from_user.id, f"🏆{day}")
    bot.send_message(message.from_user.id, f"🍺{evening}")
    bot.send_message(message.from_user.id, f"🌛{night}")

def pomodoro_work(message):
    bot.send_message(message.from_user.id, "Road to The Dream")
    bot.send_message(message.from_user.id, "Начинаем!")
    bot.send_message(message.from_user.id, "На старт!")
    bot.send_message(message.from_user.id, "Внимание!")
    bot.send_message(message.from_user.id, "Марш!")
    for i in range(1,5):
        time.sleep(5*60)
        bot.send_message(message.from_user.id, f"Прошло {i*5} минут!")
    bot.send_message(message.from_user.id, "Время!!!")
     
def pomodoro_chill(message):
    bot.send_message(message.from_user.id, choice(chill_phrasess))
    time.sleep(5*60)
    bot.send_message(message.from_user.id, "Отдых завершен!")

def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            print('Converting audio transcripts into text ...')
            print(text)
            return text
        except:
            print('Sorry.. run again...')
            return "Извени пожавуста не понял..."

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full="./voice/"+filename+".ogg"
    file_name_full_converted="./ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    text=recognise(file_name_full_converted)
    if 'прогноз' in text or 'погод' in text:
        weather_report(message)
    elif text == 'помидор':
        pomodoro_work(message)
        pomodoro_chill(message)
    elif 'курс' in text or 'валют' in text:
        currency_rate(message)
    elif 'анекдот' in text or 'прикол' in text or 'шутк' in text:
        bot.send_message(message.from_user.id, get_jokes())
    elif text == 'идинахуй' or text == 'иди нахуй':
        bot.send_message(message.from_user.id, "сам иди черт немытый")
    else:
        bot.send_message(message.from_user.id, "Извени, Босс, не понимаю, что ты хочешь пук 😔\nМожешь повторить? 🥸")
    os.remove(file_name_full)
    os.remove(file_name_full_converted)

@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("🌏 Прогноз погоды")
    btn2 = telebot.types.KeyboardButton("🍅 Помодоро")
    btn3 = telebot.types.KeyboardButton("🤡 Анекдот")
    btn4 = telebot.types.KeyboardButton("🤑 Курс валют")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    # markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Что ты хочешь, дорогой?)".format(message.from_user), reply_markup=markup)

#метод для получения текстовых сообщений
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == '🌏 Прогноз погоды':
        weather_report(message)
    elif message.text == '🍅 Помодоро':
        pomodoro_work(message)
        pomodoro_chill(message)
    elif message.text == "🤡 Анекдот":
        bot.send_message(message.from_user.id, get_jokes())
    elif message.text == "🤑 Курс валют":
        currency_rate(message)
    elif message.text == 'Иди нахуй':
        bot.send_message(message.from_user.id, "сам иди черт немытый")
    else:
        bot.send_message(message.from_user.id, 'Старого пса новым трюкам не научишь! 🐺\n' +
        'Прошу выберите из имеющегося списка 😋')

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=1)
