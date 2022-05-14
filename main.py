import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import time
from random import choice


url = 'https://yandex.kz/pogoda/karaganda/details?via=mf#28'
response = requests.get(url)

chill_phrasess = ['Зачилься браток! Заслужил', 'Ты чертова машина! Остановись, иначе уничтожишь планету своей продуктивностью',
                  'Пацаны не гоните!\n\nВы матерям нужны!']

bs = BeautifulSoup(response.text, 'lxml')

whats_day = bs.find('span', class_='a11y-hidden')
table_temp_ = bs.find_all('div', class_='weather-table__temp')
temp_value_ = bs.find_all('span', class_='temp__value temp__value_with-unit')

morning = f"Утром температура от {table_temp_[0].text.replace('…',' до ')}, ощущается как {temp_value_[0].text}"
day = f"Днем температура от  {table_temp_[1].text.replace('…',' до ')}, ощущается как {temp_value_[1].text}"
evening = f"Вечером температура от {table_temp_[2].text.replace('…',' до ')}, ощущается как {temp_value_[2].text}"
night = f"Ночью температура от {table_temp_[3].text.replace('…',' до ')}, ощущается как {temp_value_[3].text}"

print("Работаем")
bot = telebot.TeleBot('5360419753:AAFdMc5-n1bAu4IePqT3K_P3fJwE4coY_Ow')

def pomodoro_work(message):
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

@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🌏 Прогноз погоды")
    btn2 = types.KeyboardButton("🍅 Помодоро")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Что ты хочеш, дорогой?)".format(message.from_user), reply_markup=markup)

#метод для получения текстовых сообщений
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == '🌏 Прогноз погоды':
        bot.send_message(message.from_user.id, "Прогноз погоды чееееек")
        bot.send_message(message.from_user.id, f"{whats_day.text.replace(',', '').capitalize()}")
        bot.send_message(message.from_user.id, f"🌞{morning}")
        bot.send_message(message.from_user.id, f"🏆{day}")
        bot.send_message(message.from_user.id, f"🍺{evening}")
        bot.send_message(message.from_user.id, f"🌛{night}")
    elif message.text == '🍅 Помодоро':
        bot.send_message(message.from_user.id, "Road to The Dream")
        bot.send_message(message.from_user.id, "Начинаем!")
        pomodoro_work(message)
        pomodoro_chill(message)

    elif message.text == 'Иди нахуй':
        bot.send_message(message.from_user.id, "сам иди черт немытый")

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)