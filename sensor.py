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

# camera snapshot
@bot.message_handler(commands=['cam'])
def send_camera_snashot(message):
    for k in [1,2,3,4,5,6]:
        img_file = f'/home/kostya/home_termometer/cctv/snapshots/{k}/snapshot.jpg'
        nosignal_file = '/home/kostya/home_termometer/cctv/nosignal.jpg'
        if os.path.isfile(img_file):
            bot.send_photo("-444235704", photo=open(img_file, 'rb'))
        else:
            bot.send_photo("-444235704", photo=open(nosignal_file, 'rb'))

@bot.message_handler(commands=['1'])
def send_camera_snashot(message):
    img_file = f'/home/kostya/home_termometer/cctv/snapshots/1/snapshot.jpg'
    nosignal_file = '/home/kostya/home_termometer/cctv/nosignal.jpg'
    if os.path.isfile(img_file):
        bot.send_photo("-444235704", photo=open(img_file, 'rb'))
    else:
        bot.send_photo("-444235704", photo=open(nosignal_file, 'rb'))

@bot.message_handler(commands=['2'])
def send_camera_snashot(message):
    img_file = f'/home/kostya/home_termometer/cctv/snapshots/2/snapshot.jpg'
    nosignal_file = '/home/kostya/home_termometer/cctv/nosignal.jpg'
    if os.path.isfile(img_file):
        bot.send_photo("-444235704", photo=open(img_file, 'rb'))
    else:
        bot.send_photo("-444235704", photo=open(nosignal_file, 'rb'))

@bot.message_handler(commands=['3'])
def send_camera_snashot(message):
    img_file = f'/home/kostya/home_termometer/cctv/snapshots/3/snapshot.jpg'
    nosignal_file = '/home/kostya/home_termometer/cctv/nosignal.jpg'
    if os.path.isfile(img_file):
        bot.send_photo("-444235704", photo=open(img_file, 'rb'))
    else:
        bot.send_photo("-444235704", photo=open(nosignal_file, 'rb'))


@bot.message_handler(commands=['4'])
def send_camera_snashot(message):
    img_file = f'/home/kostya/home_termometer/cctv/snapshots/4/snapshot.jpg'
    nosignal_file = '/home/kostya/home_termometer/cctv/nosignal.jpg'
    if os.path.isfile(img_file):
        bot.send_photo("-444235704", photo=open(img_file, 'rb'))
    else:
        bot.send_photo("-444235704", photo=open(nosignal_file, 'rb'))

@bot.message_handler(commands=['5'])
def send_camera_snashot(message):
    img_file = f'/home/kostya/home_termometer/cctv/snapshots/5/snapshot.jpg'
    nosignal_file = '/home/kostya/home_termometer/cctv/nosignal.jpg'
    if os.path.isfile(img_file):
        bot.send_photo("-444235704", photo=open(img_file, 'rb'))
    else:
        bot.send_photo("-444235704", photo=open(nosignal_file, 'rb'))

@bot.message_handler(commands=['6'])
def send_camera_snashot(message):
    img_file = f'/home/kostya/home_termometer/cctv/snapshots/6/snapshot.jpg'
    nosignal_file = '/home/kostya/home_termometer/cctv/nosignal.jpg'
    if os.path.isfile(img_file):
        bot.send_photo("-444235704", photo=open(img_file, 'rb'))
    else:
        bot.send_photo("-444235704", photo=open(nosignal_file, 'rb'))
        
# curre4nt temperature
@bot.message_handler(commands=['t', 'T', 'т'])
def get_temperature(message):
    bot.reply_to(message, read_data())


# temperature daily statistics
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

