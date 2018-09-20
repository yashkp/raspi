import cv2
from flask import Flask, render_template, Response,request, jsonify

class VideoCamera(object):
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
    
    def __del__(self):
        self.cam.release()
        
    
    def get_frame(self):
        ret, image = self.cam.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tostring()


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

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

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
