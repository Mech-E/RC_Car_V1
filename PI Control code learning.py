import serial
import time
import subprocess

# Starts the mpremote run command for the file on ESP32
subprocess.run(['mpremote', 'connect','auto', 'run', 'PI Control code learning.py'], check=True)
time.sleep(0.5)

ser = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(2)  # allow Pico to reboot

def send_angle(angle):
    msg = f"Set {angle}\n"
def send_angle(angle):
    msg = f"SET {angle}\n"
    print(f"[PI] Sending: {msg.strip()}")
    ser.write(msg.encode())

# Test loop

while True:
    for angle in range(0, 181, 10):
        send_angle(angle)
        time.sleep(0.1)

    for angle in range(180, -1, -10):
        send_angle(angle)
        time.sleep(0.1)
