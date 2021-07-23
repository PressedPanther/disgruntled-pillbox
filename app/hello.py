from pyimagesearch.motion_detection import singlemotiondetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask,render_template,Response
#from flask_dance.contrib.github import make_github_blueprint, github
#from werkzeug.contrib.fixers import ProxyFix
from dotenv import load_dotenv
import threading
import argparse
import datetime
import imutils
import time
import cv2
#import shh.env
outputFrame = None
lock = threading.Lock()
load_dotenv()
app = Flask(__name__)
#app.wsgi_app = ProxyFix(app.wsgi_app)
#app.secret_key = "supersekrit"
#blueprint = make_github_blueprint(
 #   client_id = os.environ.get(client_id),
  #  client_secret = os.environ.get(client_secret),
#)
#app.register_blueprint(blueprint, url_prefix="/login")
#vs = VideoStream(src=0).start()
vs = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(2.0)

@app.route('/')
def home():
    #if not github.authorized:
     #   return redirect(url_for("github.login"))
    #resp = github.get("/user")
    #assert resp.ok
    #return "You are @{login} on GitHub".format(login=resp.json()["login"]))
    return render_template('home.html')
@app.route('/',defaults={'path':''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('home.html')

@app.route('/showcase/')
def showcase():
    return render_template('showcase.html')

@app.route('/stream/')
def stream():
    return render_template('stream.html')

def detect_motion(frameCount):
    global vs, outputFrame, lock
    md = singlemotiondetector(accumWeight=0.1)
    total = 0
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width = 400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7,7), 0)

        timestamp = datetime.datetime.now()
        cv2.putText(frame,timestamp.strftime(
           "%A %d %B %Y %I:%M:%S%p"), (10,frame.shape[0] - 10),
           cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1)
        if total > frameCount:
            motion = md.detect(gray)
            if motion is not None:
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX,minY), (maxX, maxY),
                (0,0,255), 2)
                
        md.update(gray)
        total += 1

        with lock: 
            outputFrame = frame.copy()

def generate():
        global outputFrame, lock
        while True:
            with lock:
                if outputFrame is None:
                    continue
                (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

                if not flag:
                    continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ 
                bytearray(encodedImage) + b'r\n')

@app.route("/video_feed")
def video_feed():
        return Response(generate(),
        mimetype= "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int,required=True,
        help= "ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f","--frame-count", type=int, default=32,
        help = "# of frames used to construct the background model")
    args = vars(ap.parse_args())

    t = threading.Thread(target=detect_motion,args=(
        args["frame_count"],
    ))
    t.daemon = True
    t.start()
    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True,use_reloader=False)

#if __name__ == '__main__':
 #   app.run(debug=True)

#vs.stop()