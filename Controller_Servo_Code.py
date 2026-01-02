from evdev import InputDevice, categorize, ecodes
import time
import serial

gamepad = InputDevice('/dev/input/event4')
print('Listening for controller events.....')

time.sleep(1)

ser = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(2)

def send_angle(angle):
    msg = f"SET {angle}\n"
    print(f"[PI] Sending: {msg.strip()}")
    ser.write(msg.encode())

def trigger_con(raw_value):
    angle = (raw_value / 1023) * 180
    return angle

for event in gamepad.read_loop():

    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        code = absevent.event.code
        value = absevent.event.value

        print(f"Axis: {code}, Value: {value}")

        # Check for ABS_Z (axis 2)
        if code == ecodes.ABS_Z:
            angle = trigger_con(value)
            send_angle(angle)