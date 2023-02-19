import cv2
# import tensorflow as tf
import numpy as np
from time import time
import requests

move = False
moveCounter = 0

time_of_motion = 5
fps = 30

width = 128
height = 128

time_no_motion = time()
time_motion = time()

output_file = "./data/move1.dat"

def main():
    cap = cv2.VideoCapture("http://10.0.0.167:81/stream")
    # cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, fps)
    render_loop(cap)
    cap.release()
    cv2.destroyAllWindows()

def render_loop(cap):
    frame1 = get_frame(cap)
    while not pressed_esc():
        frame1 = display_process_update_frame(cap, frame1)

def display_process_update_frame(cap, frame1):
    # global outputFrame, lock
    global move, time_motion, time_no_motion, time_of_motion
    frame2 = get_frame(cap)
    kernel = np.ones((2, 2))
    diff = cv2.absdiff(src1=frame1, src2=frame2)
    diff = cv2.dilate(diff, kernel, 1)
    thresh_frame = cv2.threshold(src=diff, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]
    value = thresh_frame.sum()
    cv2.imshow('webcam', thresh_frame)
    newMove = value > 10000

    if newMove and move:
        time_motion = time()
        print("move")
    else:
        time_motion = time()
        time_no_motion = time()
        print("no move")
    
    if time_motion - time_no_motion > time_of_motion:
        time_no_motion = time()
        print("RESET")
        #--------------------------
        # send_reset()
        #--------------------------
        requests.get("http://10.0.0.1:8080/api/moved/100")
    
    move = newMove
    return frame2

def pressed_esc():
    return cv2.waitKey(30) == 27

def get_frame(cap):
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (width, height))
    return frame

if __name__ == '__main__':
    main()