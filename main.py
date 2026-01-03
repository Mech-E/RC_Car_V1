import time
import serial
from Auto_Listener import ControllerListener

ser = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(2)

def convert(raw):
    return int((raw / 1023) * 180)

def send_angle(angle):
    msg = f"SET {angle}\n"
    print(f"[PI] Sending: {msg.strip()}")
    ser.write(msg.encode())

def handle_input(input_name, value):
    print("INPUT:", input_name, value)

    if input_name == "Left Trigger":
        angle = convert(value)
        send_angle(angle)

    if input_name == "Right Trigger":
        angle = convert(value)
        send_angle(angle)
    
    if input_name == "button_a" and value == 1:
        print("Button A Pressed")

listener = ControllerListener('/dev/input/event4', handle_input)
listener.start()

while True:
    time.sleep(1)