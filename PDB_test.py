from machine import I2C, Pin
import time
import sys
import select

# -----------------------------
# PCA9685 DRIVER
# -----------------------------
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
# SERVO + RATE LIMITING
# -----------------------------
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
pca = PCA9685(i2c)
pca.set_pwm_freq(50)

SERVO_SUSPENSION = [1,2,3,4]
Steering_Channel = 0

MIN_PULSE = 150
MAX_PULSE = 600

latest_angle = None
last_update = time.ticks_ms()
update_interval = 20   # 50 Hz


def set_angle(angle):
    global last_update
    now = time.ticks_ms()
    if time.ticks_diff(now, last_update) >= update_interval:
        last_update = now

        angle = max(0, min(180, angle))
        pulse = int(MIN_PULSE + (MAX_PULSE - MIN_PULSE) * (angle / 180))

        for ch in SERVO_SUSPENSION:
            pca.set_pwm(ch, 0, pulse)


# -----------------------------
# NON-BLOCKING SERIAL READER
# -----------------------------
def read_serial():
    global latest_angle
    # Drain the serial buffer completely
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline().strip().lower()

        if line.startswith("set"):
            try:
                latest_angle = int(line.split()[1])
            except:
                pass


# -----------------------------
# MAIN LOOP (REAL-TIME)
# -----------------------------
while True:
    read_serial()

    if latest_angle is not None:
        set_angle(latest_angle)