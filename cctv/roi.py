#!/usr/bin/python3

import os
import datetime
import cv2
from skimage.metrics import structural_similarity as compare_ssim


video = cv2.VideoCapture("rtsp://admin:admin@192.168.1.10:554/live/main")
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
codec = cv2.VideoWriter_fourcc(*'XVID')
fps =int(video.get(cv2.CAP_PROP_FPS))
cap_width, cap_height = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# output = cv2.VideoWriter('test1.avi', codec, fps, (cap_width, cap_height), True)
_, first_frame = video.read()

x, y, width, height = cv2.selectROI(first_frame)
print(f'\n{x}, {y}, {width}, {height}\n\n')
        

