from os import environ
from pyimagesearch.motion_detection import singlemotiondetector
from imutils.video import VideoStream
from flask import Response
from flask import (Flask,render_template,Response,request,redirect, session)
#from flask_dance.contrib.github import make_github_blueprint, github
#from werkzeug.contrib.fixers import ProxyFix
import os
import threading
import argparse
import datetime
import imutils
import time
import cv2

#outputFrame = None
#lock = threading.Lock()
app = Flask(__name__)
app.secret_key = os.getenv("client_secret")
user = {"username": "abc", "password": "xyz"}
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

@app.route('/',methods = ['POST','GET'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user['username'] and password == user['password']:
            session['user'] = username
            return redirect('/home')
        return "<h1> Wrong username or password</h1>" 
    return render_template("login.html")
#app.wsgi_app = ProxyFix(app.wsgi_app)

#blueprint = make_github_blueprint(
 #   client_id = os.environ.get(client_id),
  #  client_secret = os.environ.get(client_secret),
#)
#app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/home')
def home():
    #if not github.authorized:
     #   return redirect(url_for("github.login"))
    #resp = github.get("/user")
    #assert resp.ok
    #return "You are @{login} on GitHub".format(login=resp.json()["login"]))
    return render_template('home.html')
@app.route('/stream/')
def stream():
    return render_template('stream.html')

def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/video_feed")
def video_feed():
        return Response(gen(video),
        mimetype= "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,threaded=True)
