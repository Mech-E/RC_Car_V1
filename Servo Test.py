from machine import Pin, PWM
servo = PWM(Pin(18), freq=50)
servo.duty_ns(1500000)  # midpoint