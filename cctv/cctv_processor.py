#!/usr/bin/python3

import sys
import os
import datetime
import cv2
from skimage.metrics import structural_similarity as compare_ssim
import sqlite3

work_path = '/home/kostya/home_termometer/cctv/'
rtsp_stream = "rtsp://admin:admin@192.168.1.10:554/live/main"

if len(sys.argv) < 2: 
    print("error: cam_id doesn't set")
    sys.exit()

cam_id = sys.argv[1]


db_file = '/home/kostya/home_termometer/temperature.db'
con = sqlite3.connect(db_file)
cur = con.cursor()

cur.execute("SELECT rtsp_stream, x, y, width, height FROM cctv where cam_id = ?", [cam_id])
results = cur.fetchall()
if len(results) == 0:
    print("error: cam_id hasn't fount in db")

rtsp_stream = results[0][0]

x, y, width, height = results[0][1], results[0][2], results[0][3], results[0][4]
log_dir = work_path + 'logs/' + cam_id
os.system('mkdir -p ' + log_dir)
print(cv2.__version__, rtsp_stream, x, y, width, height)

def logmsg(msg):
    with open(log_dir + "/cctv.log", "a") as log:
        log.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - {msg}\n")


def difference(frame1, frame2):
    try:
        # convert the images to grayscale
        grayA = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        medianA = cv2.medianBlur(grayA ,5)
        grayB = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        medianB = cv2.medianBlur(grayB ,5)
        # compute the Structural Similarity Index (SSIM) between the two
        # images, ensuring that the difference image is returned
        (score, diff) = compare_ssim(medianA, medianB, full=True)
        diff = (diff * 255).astype("uint8")
        # print("SSIM: {}".format(score))
        return score
    except Exception as e:
        print(e)


while 1:
    logmsg('started')
    try:
        video = cv2.VideoCapture(rtsp_stream)
        logmsg('video loaded OK')
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        codec = cv2.VideoWriter_fourcc(*'XVID')
        fps =int(video.get(cv2.CAP_PROP_FPS))
        cap_width, cap_height = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))        
        _, first_frame = video.read()

        # show ROI to user:
        #x, y, width, height = cv2.selectROI(first_frame)
        #print(x, y, width, height)
        if (not height) and (not width):
            height, width, channels = first_frame.shape
        roi = first_frame[y: y + height, x: x + width]

        snapshot_file = 'snapshot.jpg'
        snapshot_dir = work_path + 'snapshots/' + cam_id
        os.system('mkdir -p ' + snapshot_dir)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(first_frame, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), (10,450), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(snapshot_dir + '/' + snapshot_file, first_frame) 
        print('saved')

        k = 0 
        while k < 200:
            k += 1
            _, frame = video.read()
            if frame is None:
                continue
            roi_new = frame[y: y + height, x: x + width]
            
            similarity = difference(roi, roi_new)
            if similarity < 0.8:
                dir_name = work_path + 'detections/' + cam_id + '/' + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')
                file_name = dir_name + '/' + datetime.datetime.now().strftime('%H:%M:%S') + '_' + str(k) + '.jpg'
                os.system('mkdir -p ' + dir_name)
                print(f'Detection ' + file_name)
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)
                cv2.imwrite(file_name, frame)

        # output.release()
        video.release()
    except Exception as e:
	    print(e)
        logmsg(e)
