import pandas as pd
import numpy as np
import csv
from flask import Flask, render_template,request,redirect, url_for
app = Flask(__name__)

start = False

@app.route('/index', methods=["POST","GET"])
def index():
    if request.method == "POST":
        date = request.form["date"]
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

@app.route('/application')
def application():
    return render_template('application.html')