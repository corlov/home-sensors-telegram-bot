import requests
import os
import sqlite3
import datetime
import re


home_dir = '/home/kostya/home_termometer'
log_file = f'{home_dir}/temperature.log'
db_file = f'{home_dir}/temperature.db'
token = "1209017671:AAH8evw44Tlf-eTtIXGwiOCklqiNOa0r3XA"
chat_id = "-444235704"

def send_msg(text): 
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
   results = requests.get(url_req)
   print(results.json())


def main():
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS temperature(timestamp real, t real)")


    # если данных в БД не было бол 10 минут, то значит скоее всего отключали электропиние, сообщеаем что оно восстановлено
    cur_ts = int((datetime.datetime.now().timestamp())) + 3*60*60
    cur.execute("select 1 as ex from temperature where timestamp > ? limit 1", [cur_ts - 10*60])
    results = cur.fetchall()
    if not len(results):
        send_msg("Было отключение электропитания бол 10 минут, сейчас питание восстановлено")

    last_line = ''
    t = ''
    with open(log_file, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = re.sub('[^A-Za-z0-9\.]+', '', line)
            if line:
                if float(line) > -40 and float(line) < 60:
                    t = line
    if not t:
        print(f"{last_line} temperature is unknown")
        quit()

    ts = os.path.getctime(log_file) + 3*60*60
    cur.execute("INSERT INTO temperature (timestamp, t ) VALUES (?, ?)", [ts, t])
    con.commit()

    cur.execute("SELECT t FROM temperature where timestamp < ? and timestamp > ? limit 1", [ts - 60*60, ts - 120*60])
    results = cur.fetchall()
    if len(results) > 0:
        old_t = float(results[0][0])
        d = abs(float(t) - old_t)
        if d > 2:
            send_msg(f"Внимание, температура значительно изменилась, delta = {round(d, 2)}")

    if float(t) < 5:
        send_msg(f'Критически низкая температура: {t}°C')
    elif float(t) > 35:
        send_msg(f'High temperature!!! Fire? {t} C')
    else:
        m = int(datetime.datetime.now().strftime('%M'))
        if m > 28 and m < 32:
            send_msg(f'Температура ОК: {float(t)}°C')
    
if __name__ == '__main__':
    main()
