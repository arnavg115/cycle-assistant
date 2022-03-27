import io
import socketio
import threading

import pynmea2
import serial


ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
serialio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


sio = socketio.Client()
sio.connect("http://192.168.1.94:3000/")
sio.emit("join",{"uname":"pi"})

al = []

def gps():
	global ser
	global serialio		
	while 1:
		try:
			line = serialio.readline()
			msg = pynmea2.parse(line)
			print(msg)
		except pynmea2.ParseError as e:
			print(f"PARSER: {e}")
			pass
		except serial.SerialException as e:

			print(f"DEVICE: {e}")

			ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
			serialio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

			pass

x = threading.Thread(target=gps)
x.start()

@sio.event
def msg(data):
	print(al)
	sio.emit("response","s")
	# print(data)

sio.wait()