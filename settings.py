MODE = 0 # 0 - управлять джойстиком , 1 - следовать за цветом, 3 - debug

FPS_LIMIT = False
FPS_LIMIT_VALUE = 0.01

FRAME_WIDTH = 320 #320 
FRAME_HEIGHT = 240 #240
FRAME_RESOLUTION = (320, 240)  #180,120 (если видео тупит, можно уменьшить еще больше)


BINARY_ONE = ('42', '77', '128')
BINARY_TWO = ('130', '255', '255')
MOMENTS_PIXELS = 30

SPEED_SCALE = 1.0  # speed (%) (0.50 = 50%) 
MAX_ABS_SPEED = 100  # max abs speed
SEND_FREQ = 10  # 10 packages per sec

IP = '192.168.1.64' #127.0.0.1
PORT = 5000 #5000
SERIAL_PT = '/dev/ttyUSB0' #/dev/ttyUSB0
SERIAL_UART = 9600

'''
Пресеты:
Красная указка
BINARY_O1NE = [(0, 60, 70), (10, 255, 255)] # upper color  
BINARY_T1WO = [(160, 60, 70), (179, 255, 255)] # lower color


#binary = cv2.inRange(hsv, (18, 60, 100), (32, 255, 255))  # пороговая обработка кадра (выделяем все желтое)
#binary = cv2.inRange(hsv, (0, 0, 0), (255, 255, 35))  # пороговая обработка кадра (выделяем все черное)
'''

