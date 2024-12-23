import sqlite3
import pprint



home_dir = '/home/kostya/home_termometer'
db_file = f'{home_dir}/temperature.db'


con = sqlite3.connect(db_file)
cur = con.cursor()
cur.execute("""DROP TABLE if exists cctv""")
cur.execute("""
CREATE TABLE IF NOT EXISTS cctv(
    cam_id integer, 
    rtsp_stream text,
    ip text,
    x integer,
    y integer, 
    width integer, 
    height integer
    )
""")

cur.execute("INSERT INTO cctv (cam_id, rtsp_stream, ip, x, y, width, height) VALUES (?, ?, ?, ?, ?, ?, ?)", 
    [1, 
    "rtsp://admin:admin@192.168.1.10:554/live/main", 
    "192.168.1.10", 374, 29, 722, 677])

cur.execute("INSERT INTO cctv (cam_id, rtsp_stream, ip, x, y, width, height) VALUES (?, ?, ?, ?, ?, ?, ?)", 
    [2, 
    "rtsp://192.168.1.12:554/user=admin_password=_channel=1_stream=0.sdp", 
    "192.168.1.12", 0, 0, 0, 0])


cur.execute("INSERT INTO cctv (cam_id, rtsp_stream, ip, x, y, width, height) VALUES (?, ?, ?, ?, ?, ?, ?)", 
    [3, 
    "rtsp://192.168.1.13:554/user=admin_password=_channel=1_stream=0.sdp", 
    "192.168.1.13", 0, 0, 0, 0])

cur.execute("INSERT INTO cctv (cam_id, rtsp_stream, ip, x, y, width, height) VALUES (?, ?, ?, ?, ?, ?, ?)", 
    [4, 
    "rtsp://admin:admin@192.168.1.14:554/live", 
    "192.168.1.14", 0, 0, 0, 0])


cur.execute("INSERT INTO cctv (cam_id, rtsp_stream, ip, x, y, width, height) VALUES (?, ?, ?, ?, ?, ?, ?)", 
    [5, 
    "rtsp://192.168.1.15:554/user=admin_password=_channel=1_stream=0.sdp", 
    "192.168.1.15", 0, 0, 0, 0])

cur.execute("INSERT INTO cctv (cam_id, rtsp_stream, ip, x, y, width, height) VALUES (?, ?, ?, ?, ?, ?, ?)", 
    [6, 
    "rtsp://192.168.1.16:554/user=admin_password=_channel=1_stream=0.sdp", 
    "192.168.1.16", 0, 0, 0, 0])

con.commit()

cur.execute("SELECT * FROM cctv")
results = cur.fetchall()
pprint.pprint(results)