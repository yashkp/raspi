import cv2
from flask import Flask, render_template, Response,request, jsonify
import time

camy = cv2.VideoCapture(0)#
#cam.set(3, 480)
#cam.set(4, 640)


class VideoCamera(object):
    def __init__(self):
        x = 3
        #global cam
    
    def __del__(self):
        y=3
        #cam.release()
        
    
    def get_frame(self):
        #global cam
        #ret, image = cam.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tostring()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        #frame = camera.get_frame()
        time.sleep(0.05)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    #global cam
    try:
        return Response(gen(VideoCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    finally:
        x = 5
        #cam.release()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=False)
