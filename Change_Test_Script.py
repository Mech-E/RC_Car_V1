import serial
import time
import subprocess

# Start ESP32 script without blocking
proc = subprocess.Popen(['mpremote', 'connect', 'auto', 'run', 'MicroPython_Servo_Learning.py'])

time.sleep(1)  # give ESP32 time to boot and start listening

ser = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(2)

def send_angle(angle):
    msg = f"SET {angle}\n"
    print(f"[PI] Sending: {msg.strip()}")
    ser.write(msg.encode())

while True:
    for angle in range(0, 181, 10):
        send_angle(angle)
        time.sleep(0.1)

    for angle in range(180, -1, -10):
        send_angle(angle)
        time.sleep(0.1)