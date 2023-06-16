import pandas as pd
import numpy as np
import csv
import cv2
import random
import time
from flask import Flask, render_template, request, redirect, url_for, Response,jsonify

app = Flask(__name__)

people_count = 0  # 初始化人数

@app.route('/index', methods=["POST", "GET"])
def index():
    global start
    if request.method == "POST":
        date = request.form["scale"]
        locate = request.form["locate"]
        area = request.form["area"]
        rtsp = request.form["rtsp"]
        print(date)
        print(locate)
        print(area)
        print(rtsp)
        start = True
        print(start) 

    return render_template('index.html')

def detect():
    return random.randint(0, 100)

def gen():
    global people_count
    frame_count = -1
    video_path = '..\\成醫人流辨識\\video\\ipcam固定點1-集合2.mp4'
    vid = cv2.VideoCapture(video_path)
    while True:
        return_value, frame = vid.read()
        if return_value:
            if frame_count < 0:
                frame_count = 30

            people_count = detect()
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间

            resized_frame = cv2.resize(frame, (800, 600))
            image = cv2.imencode('.jpg', resized_frame)[1].tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n'
                   b'people_count: ' + str(people_count).encode() + b'\r\n'
                   b'current_time: ' + str(current_time).encode() + b'\r\n')

            frame_count -= 1
        else:
            break

@app.route('/application', methods=["POST", "GET"])
def application():
    global people_count
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间
    return render_template('application.html', current_time=current_time, people_count=people_count)

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/get_people_count', methods=["GET"])
def get_people_count():
    def generate():
        while True:
            yield f"data: {people_count}\n\n"
            time.sleep(3)  # 可调整更新间隔时间

    return Response(generate(), mimetype='text/event-stream')