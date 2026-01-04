import time
import serial
from Auto_Listener import ControllerListener

ser = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(2)

def convert(raw):
    return int((raw / 1023) * 180)

# Servo Angle Function
def send_angle(angle):
    msg = f"SET {angle}\n"
    print(f"[PI] Sending: {msg.strip()}")
    ser.write(msg.encode())

current_trig_ang = 0
locked_ang = None

def handle_input(input_name, value):
    global current_trig_ang, locked_ang
    print("INPUT:", input_name, value)

    if input_name == "Left Trigger":
        current_trig_ang = convert(value)
        send_angle(current_trig_ang)
        print(f"Trigger angle = {current_trig_ang}")
        return

    if input_name == "Button A" and value == 1:
        locked_ang = current_trig_ang
        print(f"[LCOK] Servo set to {locked_ang}")
        send_angle(locked_ang)
        return
    
    if input_name == "Button B" and value == 1:
        locked_ang = None
        print("[RESET] Servo set to 0")
        send_angle(0)
        return
    

listener = ControllerListener('/dev/input/event4', handle_input)
listener.start()

while True:
    time.sleep(1)