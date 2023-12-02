import requests
import os
import sqlite3
import datetime


home_dir = '/home/kostya/home_termometer'
log_file = f'{home_dir}/temperature.log'
db_file = f'{home_dir}/temperature.db'
token = "1209017671:AAH8evw44Tlf-eTtIXGwiOCklqiNOa0r3XA"
chat_id = "-444235704"

def send_msg(text):   
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
   results = requests.get(url_req)
   #print(results.json())

def main():
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS temperature(timestamp real, t real)")
        
    with open(log_file) as f:
        t = f.readline()
    ts = os.path.getctime(log_file)    

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
    else:
        m = int(datetime.datetime.now().strftime('%M'))
        if m > 28 and m < 32:
            send_msg(f'Температура ОК: {float(t)}°C')
    
if __name__ == '__main__':
    main()
