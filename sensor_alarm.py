import requests
import os
import time
import datetime as dt
   
def send_msg(text):
   token = "1209017671:AAH8evw44Tlf-eTtIXGwiOCklqiNOa0r3XA"
   chat_id = "-444235704"
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
   results = requests.get(url_req)
   print(results.json())

#send_msg("Hello there!")

    
import sqlite3
time.sleep(2)

con = sqlite3.connect("/home/kostya/home_termometer/temperature.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS temperature(timestamp real, t real)")

log_file = '/home/kostya/home_termometer/temperature.log'


    
with open(log_file) as f:
        for line in f:
            pass
t = line
ts = os.path.getctime(log_file)
print('t=', t, 'ts=',ts)

cur.execute("INSERT INTO temperature (timestamp, t ) VALUES (?, ?)", [ts, t])
con.commit()

res = cur.execute("SELECT t FROM temperature where timestamp < ? and timestamp > ? limit 1", [ts - 60*60, ts - 120*60])
if res.fetchone():
    old_t = res.fetchone()[0]
    if t - old_t < -3:
        print('Сообщение о существенном падении температуры')

if float(t) < 5:
    print('Сообщение о низкой температуре')


