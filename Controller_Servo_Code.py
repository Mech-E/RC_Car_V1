from evdev import InputDevice, categorize, ecodes
import time
import subprocess
import serial
# Find the controller path: ls /dev/input/

gamepad = InputDevice('/dev/input/event4') 
print('Listening for controller events.....')

time.sleep(1)  # give ESP32 time to boot and start listening

ser = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(2)

def send_angle(angle):
    msg = f"SET {angle}\n"
    print(f"[PI] Sending: {msg.strip()}")
    ser.write(msg.encode())

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        print(f"Button: {keyevent.keycode}, State: {keyevent.keystate}")

    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        print(f"Axis: {absevent.event.code}, Value: {absevent.event.value}")

    if absevent.event.code == '2':
        angle = (absevent.event.value/1023)*180
        send_angle(angle)

        
