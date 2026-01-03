import threading
from evdev import InputDevice, categorize, ecodes

class ControllerListener:
    def __init__(self, device_path, callback):
        self.gamepad = InputDevice(device_path)
        self.callback = callback # Function to call when axis changes
        self.thread = None
        self.running = False

        def start(self):
            print("Listening for controller input...")

            for event in self.gamepad.read_loop():
                if event.type != ecodes.EV_ABS:
                    continue

                absevent = categorize
                code = absevent.event.code
                value = absevent.event.value

                # Only put axis we care about

                if code == ecodes.ABS_Z:
                    self.callback(value)
        
        def start(self):
            """Start the listner in a background thread"""
            if self.thread is None:
                self.running = True
                self.thread = threading.Thread(target=self._listen, daemon=True)
                self.thread.start()

        def stop(self):
            """Stop listener cleanly"""
            self.running = False