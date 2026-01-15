# -----------------------------
# PCA9685 DRIVER (embedded)
# -----------------------------
from machine import I2C, Pin
import time

class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.reset()

    def reset(self):
        self.write8(0x00, 0x00)

    def write8(self, reg, value):
        self.i2c.writeto_mem(self.address, reg, bytes([value]))

    def set_pwm_freq(self, freq):
        prescale = int(25000000.0 / (4096 * freq) - 1)
        oldmode = self.i2c.readfrom_mem(self.address, 0x00, 1)[0]
        newmode = (oldmode & 0x7F) | 0x10
        self.write8(0x00, newmode)
        self.write8(0xFE, prescale)
        self.write8(0x00, oldmode)
        time.sleep_ms(5)
        self.write8(0x00, oldmode | 0xa1)

    def set_pwm(self, channel, on, off):
        data = bytearray([on & 0xFF, on >> 8, off & 0xFF, off >> 8])
        self.i2c.writeto_mem(self.address, 0x06 + 4 * channel, data)

# -----------------------------
# SERVO CONTROL
# -----------------------------

i2c = I2C(0, sda=Pin(0), scl=Pin(1))
pca = PCA9685(i2c)
pca.set_pwm_freq(50)

SERVO_CH = 1

# Typical servo pulse range for PCA9685
MIN_PULSE = 150   # 0 degrees
MAX_PULSE = 600   # 180 degrees

def set_angle(angle):
    pulse = int(MIN_PULSE + (MAX_PULSE - MIN_PULSE) * (angle / 180))
    pca.set_pwm(SERVO_CH, 0, pulse)

# Sweep 0 → 180 → 0 forever
while True:
    for angle in range(0, 181, 5):
        set_angle(angle)
        time.sleep(0.02)

    for angle in range(180, -1, 5):
        set_angle(angle)
        time.sleep(0.02)