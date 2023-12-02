import os
import telebot
import time
import datetime as dt

bot = telebot.TeleBot('1209017671:AAH8evw44Tlf-eTtIXGwiOCklqiNOa0r3XA')
log_file = '/home/kostya/home_termometer/temperature.log'

def read_data():
    with open(log_file) as f:
        for line in f:
            pass
    last_line = line
    t = dt.datetime.fromtimestamp(os.path.getctime(log_file))
    return t.strftime("%d.%m.%Y %H:%M") + ', ' + last_line[:-1] + "°C"


@bot.message_handler(commands=['t', 'T', 'т'])
def get_temperature(message):
    bot.reply_to(message, read_data())

    
bot.infinity_polling()

