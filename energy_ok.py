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
    send_msg("Power OK")
   


if __name__ == '__main__':
    main()
