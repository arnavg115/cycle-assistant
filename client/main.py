import socketio
from gpiozero import Button
sio = socketio.Client()
sio.connect("")

button = Button(2)
@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')
while True:
    if button.is_pressed:
        sio.emit("button_pressed",{"pressed":"yes"})






