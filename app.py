from flask import Flask, render_template, Response, redirect, request, url_for
from camera import WebcamVideoStream
from plateProcessing import PlateProcessing
from db import DB
from werkzeug.utils import secure_filename
from vehicle import Vehicle
from cctv import CCTV
import cv2
import os
import time

app = Flask(__name__)
db = DB()
cap = WebcamVideoStream()

UPLOAD_FOLDER = ('static/img/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/start_stream')
def start_stream():
    if str(db.getRTSP_cctv()) is '0':
        print(str(db.getRTSP_cctv()))
        cap.start()
    else:
        src_rtsp = str(db.getRTSP_cctv())
        cap.start(src=src_rtsp)
    print(' * License Plate Processing is started...!!!')
    print(' * RTSP : ' + str(db.getRTSP_cctv()))
    return redirect(url_for('index')) 
@app.route('/stop_stream')
def stop_stream():
    cap.stop()
    print(' * License Plate Processing is stoped...!!!')
    print(' * RTSP : ' + str(db.getRTSP_cctv()))
    return redirect(url_for('index'))

@app.route('/')
def index():
    """Video streaming home page."""
    vehicle_data = db.getAll_vehicle()
    cctv_data = db.getAll_cctv()

    return render_template('index.html', datas = vehicle_data, datas1 = cctv_data)

@app.route('/insert_lp', methods=['POST'])
def insert_lp():
    vehicle = Vehicle()
    if request.method == 'POST':
        vehicle.set_plate(request.form['plate'])
        vehicle.set_brand(request.form['brand'])
        vehicle.set_province(request.form['province'])
        vehicle.set_color(request.form['color'])
        vehicle.set_detection_status(False)
        vehicle.set_detected_dateTime('')
        vehicle.set_img_path('')
        data = vehicle.__dict__
        db.insert_vehicle(data)
    return redirect(url_for('index'))

@app.route('/update_lp', methods=['POST'])
def update_lp():
    vehicle = Vehicle()
    if request.method == 'POST':
        objId = request.form['objId']
        vehicle.set_plate(request.form['plate'])
        vehicle.set_brand(request.form['brand'])
        vehicle.set_province(request.form['province'])
        vehicle.set_color(request.form['color'])
        vehicle.set_detection_status(False)
        vehicle.set_detected_dateTime('')
        vehicle.set_img_path('')
        data = vehicle.__dict__
        db.update_vechicle(objId, data)
    return redirect(url_for('index'))

@app.route('/delete/<string:objId>', methods=['GET'])
def delete_lp(objId):
    db.delete_vehicle(objId)
    return redirect(url_for('index'))

@app.route('/cctv_rtsp', methods=['POST'])
def cctv_rtsp():
    cap.stop()
    print(' * License Plate Processing is stoped...!!!')
    print(' * RTSP : ' + str(db.getRTSP_cctv()))

    cctv = CCTV()
    if request.method == 'POST':
        objId = request.form['objId']
        cctv.set_rtsp(request.form['stream_src'])
        print(' * RTSP is updated : ' + cctv.get_rtsp())
        data = cctv.__dict__ 
        db.update_cctv(objId, data)
    return redirect(url_for('index'))

def gen_frame():
    """Video streaming generator function."""
    img_processed = PlateProcessing()
    bg_stream = cv2.imread('static/img/bg/bg-home2.jpg')
    bgs = cv2.imencode('.jpg', bg_stream)[1].tobytes()

    if cap.started is False:
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + bgs + b'\r\n') 

    while cap.started:
        frame = cap.read()
        licensePlateDetection, _ = img_processed.plateProcessing(frame)
        if cap.started is True:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + licensePlateDetection + b'\r\n') # concate frame one by one and show result

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



def get_img(_img_processed):   
    yield (b'--_img_processed\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + _img_processed + b'\r\n')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
    _saved = False
    _img_path = ''
    if request.method == 'POST':
        img_file = request.files['file']

        if img_file and allowed_file(img_file.filename):
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_file.filename))

            _img_path = img_file.filename

            _img_process = PlateProcessing()
            _img = cv2.imread('static/img/uploads/'+_img_path)
            _img_processed, _imgWrite = _img_process.plateProcessing(_img)
            cv2.imwrite('output.jpg', _imgWrite)
            time.sleep(2)
            return Response(get_img(_img_processed),
                    mimetype='multipart/x-mixed-replace; boundary=_img_processed')
    
    return redirect(url_for('index'))
             

# app.route('/img_processed')
# def img_processed():
#     _img_process = PlateProcessing()
#     _img = cv2.imread('static/img/uploads/'+_img_path)
#     # if _saved is True:
#     _img_processed = _img_process.plateProcessing(_img)
#     return Response(get_img(_img_processed),
#         mimetype='multipart/x-mixed-replace; boundary=_img_processed')    

if __name__ == '__main__':
    cctv = CCTV()
    cctv.set_rtsp('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')
    print(id(cctv))
    data = cctv.__dict__
    print(data)

    nnn = DB()
    nnn.insert_cctv(data)
    x = nnn.getAll_cctv()
    print(x)
    # y = nnn.getAll_vehicle()
    # print(y)
    # nnn.delete_cctv('5ea924ef5a410e444b8af9e4')

    app.run(debug=True, threaded=True)