import cv2
from flask import Flask, render_template, Response,request, jsonify

#
#cam.set(3, 480)
#cam.set(4, 640)


class VideoCamera(object):
    def __init__(self):
        global cam
        self.cam = self.camera_obj()
        #global cam
    
    def __del__(self):
        self.cam.release()
        #cam.release()

    def camera_obj(self):
        global cam, flag
        if flag is False:
            cam = cv2.VideoCapture(0)
            return cam
        else:
            return cam
    
    def get_frame(self):
        ret, image = self.cam.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tostring()

cam = None
flag = False
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
