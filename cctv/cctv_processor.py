#!/usr/bin/python3

import os
import datetime
import cv2
from skimage.metrics import structural_similarity as compare_ssim

print(cv2.__version__)

def logmsg(msg):
    with open("/home/kostya/home_termometer/cctv/cctv.log", "a") as log:
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
        video = cv2.VideoCapture("rtsp://admin:admin@192.168.1.10:554/live/main")
        logmsg('video loaded OK')
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        codec = cv2.VideoWriter_fourcc(*'XVID')
        fps =int(video.get(cv2.CAP_PROP_FPS))
        cap_width, cap_height = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        _, first_frame = video.read()

        x, y, width, height = 374, 29, 722, 677
        roi = first_frame[y: y + height, x: x + width]

        k = 0 
        while k < 200:
            k += 1
            _, frame = video.read()
            if frame is None:
                continue
            roi_new = frame[y: y + height, x: x + width]
            
            similarity = difference(roi, roi_new)
            if similarity < 0.8:
                dir_name = '/home/kostya/home_termometer/cctv/detections/' + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')
                file_name = dir_name + '/' + datetime.datetime.now().strftime('%H:%M:%S') + '_' + str(k) + '.jpg'
                os.system('mkdir -p ' + dir_name)
                print(f'Detection ' + file_name)                
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)
                cv2.imwrite(file_name, frame)

        video.release()
    except Exception as e:
        print(e)
        logmsg(e)





