from evdev import InputDevice, categorize, ecodes
import time
import serial

gamepad = InputDevice('/dev/input/event4')
print('Listening for controller events.....')

ser = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(2)

def send_angle(angle):
    msg = f"SET {angle}\n"
    print(f"[PI] Sending: {msg.strip()}")
    ser.write(msg.encode())

def convert(raw):
    # adjust this once we know your axis range
    return int((raw / 1023) * 180)

for event in gamepad.read_loop():

    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        code = absevent.event.code
        value = absevent.event.value

        print(f"Axis: {code}, Value: {value}")

        # CHANGE THIS to the correct axis
        if code == ecodes.ABS_Z:
            angle = convert(value)
            send_angle(angle)