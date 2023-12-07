import os
import telebot
import datetime as dt
import sqlite3

home_dir = '/home/kostya/home_termometer'
db_file = f'{home_dir}/temperature.db'

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


@bot.message_handler(commands=['s', 'stat', 'statistics'])
def get_temperatur_statistics(message):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    response = ''
    for row in cur.execute("""
            select 
                avg(t) as t,
                strftime('%H', DATETIME(ROUND(timestamp), 'unixepoch')) as h
            from temperature
            where
                strftime('%s', 'now') - timestamp < 60*60*24
            group by
            strftime('%H', DATETIME(ROUND(timestamp), 'unixepoch'));
        """):
        response += f'{row[1]}: {round(row[0], 2)}°C\n'
    bot.reply_to(message, response)
    
bot.infinity_polling()

