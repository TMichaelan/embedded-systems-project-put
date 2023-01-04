from flask import Flask, render_template, Response, request
import cv2
import serial
import threading
import time
import json
import argparse
import settings as stgs
import numpy as np
app = Flask(__name__)

cam = cv2.VideoCapture(0) 
cam.set(cv2.CAP_PROP_FRAME_WIDTH, stgs.FRAME_WIDTH) 
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, stgs.FRAME_HEIGHT) 

axisX, axisY = 0.0, 0.0
h1 = 0
s1 = 0
v1 = 0
h2 = 0
s2 = 0
v2 = 0
mp = 20
showContours = False

def getFrames():

    global axisX, axisY
    while True:

        if stgs.FPS_LIMIT:
            time.sleep(stgs.FPS_LIMIT_VALUE) 
        
        seeObj = False  
       
        success, frame = cam.read() 

        if success:
            frame = cv2.resize(frame, stgs.FRAME_RESOLUTION, interpolation=cv2.INTER_AREA) 
            height, width = frame.shape[0:2] 

            if stgs.MODE == 1:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
                
                h_min = np.array(stgs.BINARY_ONE, np.uint8)
                h_max = np.array(stgs.BINARY_TWO, np.uint8)
                binary = cv2.inRange(hsv, h_min, h_max)
                conts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) 

                if len(conts) != 0:  
                    max_conts = max(conts, key=cv2.contourArea)  
                    mom_conts = cv2.mom_conts(max_conts)  

                    if mom_conts["m00"] > stgs.MOMENTS_PIXELS:  
                        x_conts = int(mom_conts["m10"] / mom_conts["m00"])  
                        y_conts = int(mom_conts["m01"] / mom_conts["m00"])  
                        seeObj = True
                        axisX = 2 * (x_conts - width / 2) / width 
                        cv2.drawContours(frame, max_conts, -1, (0, 255, 0), 1)  
                        cv2.line(frame, (x_conts, 0), (x_conts, height), (0, 255, 0), 1)  
                        cv2.line(frame, (0, y_conts), (width, y_conts), (0, 255, 0), 1)  

                if seeObj and stgs.MODE != 3:    
                    axisY = 0.5  
                else:
                    axisY = 0.0  
                    axisX = 0.0  

                binary_shape = cv2.resize(binary, (int(binary.shape[1] / 4), int(binary.shape[0] / 4)),  
                                    interpolation=cv2.INTER_AREA)                                  
                binary_shape = cv2.cvtColor(binary_shape, cv2.COLOR_GRAY2BGR)                                 
                frame[-2 - binary_shape.shape[0]:-2, 2:2 + binary_shape.shape[1]] = binary_shape             

                # cv2.putText(frame, 'seeObj: {};'.format(seeObj), (width - 120, height - 5),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 0, 0), 1, cv2.LINE_AA)  
                # cv2.putText(frame, 'axisX: {:.2f}'.format(axisX), (width - 70, height - 5),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 0, 0), 1, cv2.LINE_AA)  
                
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

            elif stgs.MODE == 1 or stgs.MODE == 0:
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

            elif stgs.MODE == 3:
        
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
                h_min = np.array((h1, s1, v1), np.uint8)
                h_max = np.array((h2, s2, v2), np.uint8)
                binary = cv2.inRange(hsv, h_min, h_max)  

                if showContours:
                    conts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  

                    if len(conts) != 0:  
                        max_conts = max(conts, key=cv2.contourArea) 
                        mom_conts = cv2.mom_conts(max_conts)  

                        if mom_conts["m00"] > stgs.MOMENTS_PIXELS:  
                            x_conts = int(mom_conts["m10"] / mom_conts["m00"])  
                            y_conts = int(mom_conts["m01"] / mom_conts["m00"])  
                            seeObj = True  
                            axisX = 2 * (x_conts - width / 2) / width 
                            cv2.drawContours(frame, max_conts, -1, (0, 255, 0), 1)  
                            cv2.line(frame, (x_conts, 0), (x_conts, height), (0, 255, 0), 1)  
                            cv2.line(frame, (0, y_conts), (width, y_conts), (0, 255, 0), 1)  

                _, buffer = cv2.imencode('.jpg', frame)
                _, binary_buffer = cv2.imencode(".jpg", binary)

                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
                yield (b'--binary\r\n' b'Content-Type: image/jpeg\r\n\r\n' + binary_buffer.tobytes() + b'\r\n')


def changeHSV():

    with open("settings.py", "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "BINARY_ONE" in line:
            lines[i] = f"BINARY_ONE = {(h1,s1,v1)}\n"

        elif "BINARY_TWO" in line:
            lines[i] = f"BINARY_TWO = {(h2,s2,v2)}\n"
        elif "MOMENTS_PIXELS" in line:
            lines[i] = f"MOMENTS_PIXELS = {mp}\n"

    with open("settings.py", "w") as f:
        f.writelines(lines)


@app.route('/video_feed')
def video_feed():
    return Response(getFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if stgs.MODE == 0:
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/control')
    def control():
        global axisX, axisY
        axisX, axisY = float(request.args.get('x')) / 100.0, float(request.args.get('y')) / 100.0
        return '', 200, {'Content-Type': 'text/plain'}

elif stgs.MODE == 1:  
    @app.route('/')
    def index():
        return render_template('index1.html')


elif stgs.MODE == 3:
    
    @app.route("/process", methods=["POST"])
    def process():
        global h1,s1,v1,h2,s2,v2,showContours,mp
        
        data = request.get_json()
       
        mp = data["slider0"]
        h1 = data["slider1"]
        s1 = data["slider2"]
        v1 = data["slider3"]
        h2 = data["slider4"]
        s2 = data["slider5"]
        v2 = data["slider6"]
        showContours = data["slider7"]
        vv = data["slider8"]
        if vv:
            changeHSV()
        return 'Success'

    @app.route('/')
    def index():
        return render_template('settings.html')

@app.route('/binary_feed')
def binary_feed():  
    return Response(getFrames(), mimetype='multipart/x-mixed-replace; boundary=binary')

if __name__ == '__main__':
   
    
    uart_msg = {
        "speed_left": 0,  
        "speed_right": 0  
    }

    
   
    speed_scale = stgs.SPEED_SCALE 
    max_absolute_sp = stgs.MAX_ABS_SPEED  
    send_freq = stgs.SEND_FREQ  



    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', '--port', type=int, default=stgs.PORT, help="Running port")
    arg_parser.add_argument("-i", "--ip", type=str, default=stgs.IP, help="IP address")
    arg_parser.add_argument('-s', '--serial', type=str, default=stgs.SERIAL_PT, help="Serial port")
    args = arg_parser.parse_args()
    serialPort = serial.Serial(args.serial, stgs.SERIAL_UART)  

    def uart_send():
        global axisX, axisY


        while True:
            speed_left = max_absolute_sp * (axisY + axisX)    
            speed_right = max_absolute_sp * (axisY - axisX)    

            speed_left = max(-max_absolute_sp, min(speed_left, max_absolute_sp))   
            speed_right = max(-max_absolute_sp, min(speed_right, max_absolute_sp))    

            uart_msg["speed_left"], uart_msg["speed_right"] = speed_scale * speed_left, speed_scale * speed_right 

            serialPort.write(json.dumps(uart_msg, ensure_ascii=False).encode("utf8")) 
            time.sleep(1 / send_freq)



    threading.Thread(target=uart_send, daemon=True).start()    
    app.run(debug=False, host=args.ip, port=args.port)  
