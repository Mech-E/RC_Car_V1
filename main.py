import time
import serial
from ControllerListener import ControllerListener
from Camera_Display import CameraDisplay


ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)

# Signal Rate limiter
last_send_Susp = 0
last_send_Steer = 0
Send_interval = 0.02  # 20 ms 

def convert(raw):
    angle = int((raw / 1023) * 180)
    print(f"[DEBUG] Left Trigger raw={raw} → angle={angle}")
    return angle

def convert_steering(joystick_raw):
    angle = int(((joystick_raw + 32768) / 65535) * 180)
    print(f"[DEBUG] Steering raw={joystick_raw} → angle={angle}")
    return angle

def Send_Steering(angle):
    global last_send_Steer
    now = time.monotonic()
    if now - last_send_Steer >= Send_interval:
        msg = f"STEER {angle}\n"
        ser.write(msg.encode())
        last_send_Steer = now
        print(f"[SEND] Steering → {msg.strip()}")
    else:
        print(f"[SKIP] Steering rate-limited (angle={angle})")

def Send_Suspension(angle):
    global last_send_Susp
    now = time.monotonic()
    if now - last_send_Susp >= Send_interval:
        msg = f"SET {angle}\n"
        ser.write(msg.encode())
        last_send_Susp = now
        print(f"[SEND] Suspension → {msg.strip()}")
    else:
        print(f"[SKIP] Suspension rate-limited (angle={angle})")

current_trig_ang = 0
locked_ang = None

def handle_input(input_name, value):
    global current_trig_ang, locked_ang

    print(f"[INPUT] {input_name}: {value}")

    if input_name == "Left Trigger":
        current_trig_ang = convert(value)

        angle_to_send = locked_ang if locked_ang is not None else current_trig_ang
        print(f"[STATE] Suspension angle_to_send={angle_to_send} (locked={locked_ang})")
        Send_Suspension(angle_to_send)
        return

    if input_name == "Button A" and value == 1:
        locked_ang = current_trig_ang
        print(f"[LOCK] Suspension locked at {locked_ang}")
        Send_Suspension(locked_ang)
        return
    
    if input_name == "Button B" and value == 1:
        print("[UNLOCK] Suspension unlocked, resetting to 0")
        locked_ang = None
        Send_Suspension(0)
        return
    
    if input_name == "Right Joystick Horizontal":
        steering_angle = convert_steering(value)
        Send_Steering(steering_angle)
        print(f"[DEBUG] Steering Angle Sent: {steering_angle}")
        return

listener = ControllerListener('/dev/input/event4', handle_input)
listener.start()

# Clean kill of the program
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nClosing serial connection...")
    ser.close() 
    print("Done.")