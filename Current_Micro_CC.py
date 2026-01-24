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
        print("[INIT] PCA9685 initializing...")
        self.reset()
        print("[INIT] PCA9685 ready.")

    def reset(self):
        print("[PCA9685] Resetting chip...")
        self.write8(0x00, 0x00)

    def write8(self, reg, value):
        # Debug low-level register writes
        print(f"[I2C] Write reg=0x{reg:02X}, value=0x{value:02X}")
        self.i2c.writeto_mem(self.address, reg, bytes([value]))

    def set_pwm_freq(self, freq):
        print(f"[PCA9685] Setting PWM frequency to {freq} Hz")
        prescale = int(25000000.0 / (4096 * freq) - 1)
        oldmode = self.i2c.readfrom_mem(self.address, 0x00, 1)[0]
        newmode = (oldmode & 0x7F) | 0x10
        self.write8(0x00, newmode)
        self.write8(0xFE, prescale)
        self.write8(0x00, oldmode)
        time.sleep_ms(5)
        self.write8(0x00, oldmode | 0xa1)
        print(f"[PCA9685] Prescale set to {prescale}")

    def set_pwm(self, channel, on, off):
        print(f"[PWM] CH={channel} ON={on} OFF={off}")
        data = bytearray([on & 0xFF, on >> 8, off & 0xFF, off >> 8])
        self.i2c.writeto_mem(self.address, 0x06 + 4 * channel, data)


# -----------------------------
# SERVO CONFIG
# -----------------------------
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
pca = PCA9685(i2c)
pca.set_pwm_freq(50)

SERVO_SUSPENSION = [1, 2, 3, 4]
STEERING_CHANNEL = 0

MIN_PULSE = 150
MAX_PULSE = 600


def angle_to_pulse(angle):
    clamped = max(0, min(180, angle))
    pulse = int(MIN_PULSE + (MAX_PULSE - MIN_PULSE) * (clamped / 180))
    print(f"[ANGLE] angle={angle} clamped={clamped} pulse={pulse}")
    return pulse


def set_steering(angle):
    print(f"[STEER] Setting steering to {angle}")
    pulse = angle_to_pulse(angle)
    pca.set_pwm(STEERING_CHANNEL, 0, pulse)


def set_suspension(angle):
    print(f"[SUSP] Setting suspension to {angle}")
    pulse = angle_to_pulse(angle)
    for ch in SERVO_SUSPENSION:
        print(f"[SUSP] CH={ch} pulse={pulse}")
        pca.set_pwm(ch, 0, pulse)


# -----------------------------
# NON-BLOCKING SERIAL READER
# -----------------------------
def read_serial():
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline().strip().lower()
        print(f"[SERIAL] Raw input: '{line}'")

        parts = line.split()
        if len(parts) < 2:
            print("[SERIAL] Ignored: not enough parts")
            continue

        cmd = parts[0]
        try:
            value = int(parts[1])
        except:
            print("[SERIAL] Invalid number, ignoring")
            continue

        print(f"[CMD] cmd={cmd}, value={value}")

        if cmd == "set":
            set_suspension(value)

        elif cmd == "steer":
            set_steering(value)

        else:
            print(f"[SERIAL] Unknown command '{cmd}'")


# -----------------------------
# MAIN LOOP (REAL-TIME)
# -----------------------------
print("[MAIN] Starting real-time loop...")
while True:
    read_serial()
    time.sleep_ms(5)