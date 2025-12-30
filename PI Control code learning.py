import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)  # allow Pico to reboot

def send_angle(angle):
    ser.write(f"SET {angle}\n".encode())

# Test loop
while True:
    for angle in range(0, 181, 10):
        send_angle(angle)
        time.sleep(0.1)

    for angle in range(180, -1, -10):
        send_angle(angle)
        time.sleep(0.1)
