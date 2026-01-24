from machine import Pin, PWM
import time, sys

# Setup servo on GPIO18
servo = PWM(Pin(18))
servo.freq(50)

def set_angle(angle):
    """Convert angle (0–180) to duty_ns and apply it."""
    min_us = 500
    max_us = 2500
    us = min_us + (max_us - min_us) * (angle / 180)

    duty_ns = int(us * 1000)  # convert microseconds → nanoseconds
    servo.duty_ns(duty_ns)

    print("SET:", angle, "=>", duty_ns, "ns")  # send feedback to Pi


while True:
    line = sys.stdin.readline().strip()

    if not line:
        continue

    try:
        # Expecting: "SET <angle>"
        parts = line.split()
        if len(parts) != 2:
            print("ERR: Bad command:", line)
            continue

        angle = int(parts[1])
        angle = max(0, min(180, angle))  # clamp

        print("Parsed angle:", angle)
        set_angle(angle)

    except Exception as e:
        print("ERR:", e)