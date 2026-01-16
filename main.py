import time
import serial
from ControllerListener import ControllerListener

ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)

# Signal Rate limiter
last_send = 0
Send_interval = 0.02  # 20 ms 

def convert(raw):
    return int((raw / 1023) * 180)

def convert_steering(joystick_raw):
    return int(((joystick_raw + 32768) / 65535) * 180)

def send_angle(angle):
    global last_send
    now = time.monotonic()
    if now - last_send >= Send_interval:
        msg = f"SET {angle}\n"
        ser.write(msg.encode())
        last_send = now

current_trig_ang = 0
locked_ang = None

def handle_input(input_name, value):
    global current_trig_ang, locked_ang

    if input_name == "Left Trigger":
        current_trig_ang = convert(value)

        # Always send a valid angle
        angle_to_send = locked_ang if locked_ang is not None else current_trig_ang
        send_angle(angle_to_send)
        return

    if input_name == "Button A" and value == 1:
        locked_ang = current_trig_ang
        send_angle(locked_ang)
        return
    
    if input_name == "Button B" and value == 1:
        locked_ang = None
        send_angle(0)   # IMPORTANT
        return
    
    if input_name == "Right Joystick Horizontal":
        steering_angle = convert_steering(value)
        send_angle(steering_angle)
        print(f"Steering Angle: {steering_angle}")
        return

listener = ControllerListener('/dev/input/event4', handle_input)
listener.start()

while True:
    time.sleep(1)