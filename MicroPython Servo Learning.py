from machine import Pin, PWM
import time, sys

servo = PWM(Pin(15))
servo.freq(50)

def set_angle(angle):
    min_us = 500
    max_us = 2500
    us = min_us + (angle / 180) * (max_us - min_us)
    duty = int((us / 20000) * 65535)
    servo.duty_u16(duty)

while True:
    line = sys.stdin.readline().strip()
    if line.startswith("SET"):
        try:
            angle = int(line.split()[1])
            angle = max(0, min(180, angle))
            set_angle(angle)
        except:
            pass