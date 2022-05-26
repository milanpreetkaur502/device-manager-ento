from crypt import methods
import json
from flask import Flask, render_template, Response, redirect, request, session, url_for
import cv2
import time
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY']="asdadvadfsdfs"      #random secret key
app.config['ENV']='development'
app.config['UPLOAD_FOLDER']='/media/mmcblk1p1'

def readData():
    path="/tmp/devicestats"  
    data=None
    with open(path ,'r') as file:
        data=json.load(file)

    path="/tmp/" 
    data['temperature']=None
    with open(path+'met' ,'r') as file:
        data['temperature']=file.readlines()

    data['battery_parameters']=None
    with open(path+'battery_parameters' ,'r') as file:
        data['battery_parameters']=file.readlines()

    data['light_intensity']=None
    with open(path+'light_intensity' ,'r') as file:
        data['light_intensity']=file.readlines()[0].split(":")[1:]

    return data

@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        #f.save(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        return render_template("success.html", name = f.filename)  

@app.route('/',methods=["GET","POST"])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('pass')
        credentials=None
        with open('/usr/sbin/DeviceManager/credentials.json') as file:
            credentials=json.load(file)
        if credentials['email']==email and credentials['password']==password:
            session['username']=credentials['username']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

def gen_frames():  # generate frame by frame from camera
    
    subprocess.call(["systemctl","stop","cam"])
    camera = cv2.VideoCapture(2)  # use 0 for web camera
    #camera = cv2.VideoCapture("v4l2src device=/dev/video2 ! video/x-raw, width=640, height=480 framerate=60/1, format=(string)UYVY ! decodebin ! videoconvert ! appsink", cv2.CAP_GSTREAMER)  # use 0 for web camera
    #  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
    # for local webcam use cv2.VideoCapture(0)
    while True:
        #print("kuch toh")
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        


@app.route('/video_feed')
def videoFeed():
    if 'username' in  session:
    #Video streaming route. Put this in the src attribute of an img tag
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return redirect(url_for('login'))

@app.route('/video')
def video(): 
    if 'username' in session:
        return render_template('videoFeed.html')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('Dashboard.html',data=readData())
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
