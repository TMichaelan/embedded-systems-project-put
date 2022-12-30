# embedded-systems-project

## Robot
<h1 align="center">
  <img src=https://github.com/TMichaelan/embedded-systems-project/blob/main/img/robot.jpg?raw=true width="800">
  <br>
  <img src=https://github.com/TMichaelan/embedded-systems-project/blob/main/img/binary.png?raw=true width="800">
</h1>    

## Main components:

* Web Cam
* Raspberry Pi 3
* Arduino Uno
* USB-TTL converter
* 4 wheels with motors
* 2x 18650 batteries
* motor expansion board


## Launch
The device we are going to connect to must be on the same network(Wi-Fi) with Raspberry Pi.

Download the project repository:
```shell
git clone https://github.com/TMichaelan/embedded-systems-project.git
```
Install requirements
```shell
pip install -r requirements
```

launch the application
```shell
cd embedded-systems-project
python3 app.py -i (ip-adress rasberry pi) -p (port) -s (UART)
```
or
```
in the file settings.py insert IP-address, port, uart
```
Open the browser and type in it
```shell
(ip-adress rasberry pi):(port)
```
Mobile phone:
```
http://(ip-adress rasberry pi):(port)
```
Example:
```
192.168.1.64:5000
```

 ## <a href="https://youtu.be/yCCHGjytB-s">demo video</a>

