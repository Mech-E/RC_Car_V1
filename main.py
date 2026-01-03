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

def handle_trigger(raw_value):
    angle = convert(raw_value)
    send_angle(angle)

listener = ControllerListener('/dev/input/event4', handle_trigger)
listener.start()

while True:
    time.sleep(1)