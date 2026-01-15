from machine import Pin, I2C
from pca9685 import PCA9685
import time

# Initialize I2C0 on GP0 (SDA) and GP1 (SCL)
i2c = I2C(0, sda=Pin(0), scl=Pin(1))

# Initialize PCA9685
pca = PCA9685(i2c)
pca.freq(50)  # Standard servo frequency

SERVO_CH = 1  # Servo plugged into PCA9685 channel 1

# Typical servo pulse range (adjust for your servo)
MIN = 150  # ~0°
MID = 375  # ~90°
MAX = 600  # ~180°

# Move servo on channel 1
pca.duty(SERVO_CH, MID)