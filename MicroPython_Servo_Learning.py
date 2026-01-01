from machine import Pin, PWM
import time, sys

# Use a SAFE ESP32 pin, e.g. GPIO18
servo = PWM(Pin(18), freq=50)

def set_angle(angle):
    min_us = 500
    max_us = 2500
    us = min_us + (angle / 180) * (max_us - min_us)

    # ESP32 uses nanoseconds for precise servo control
    print("Setting angle:", angle, "=>", int(us * 1000), "ns")   # <-- DEBUG
    servo.duty_ns(int(us * 1000))

while True:
    line = sys.stdin.readline().strip()

    print("Received raw:", line)   # <-- DEBUG: shows every incoming command

    if line.startswith("SET"):
        try:
            angle = int(line.split()[1])
            angle = max(0, min(180, angle))

            print("Parsed angle:", angle)   # <-- DEBUG: confirms parsing

            set_angle(angle)
        except Exception as e:
            print("Error parsing:", e)      # <-- DEBUG: catches malformed input