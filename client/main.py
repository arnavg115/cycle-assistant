import io
import socketio
import threading
import time
import pynmea2
import serial


ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
serialio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


sio = socketio.Client()
sio.connect("http://192.168.1.94:3000/")
lat = 0
lng = 0


def gps():
    global lat
    global lng
    global ser
    global serialio
    while 1:
        try:
            line = serialio.readline()
            msg = pynmea2.parse(line)

            print(type(msg))
            if type(msg) == 'pynmea2.types.talker.TXT':
                print("s")
            else:
                if "latitude" in dir(msg):
                    lat = msg.latitude
                    lng = msg.longitude
        except serial.SerialException as e:
            ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
            serialio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

            print('Device error: {}'.format(e))
            continue
        except pynmea2.ParseError as e:
            # print('Parse error: {}'.format(e))
            continue

x = threading.Thread(target=gps)
x.start()

while 1:
    if lat != 0 and lng !=0:
        sio.emit("gps",[lng, lat])
    time.sleep(0.2)

