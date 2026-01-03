import threading
from evdev import InputDevice, categorize, ecodes

class ControllerListener:
    def __init__(self, device_path, callback):
        self.gamepad = InputDevice(device_path)
        self.callback = callback
        self.thread = None
        self.running = False

    def _listen(self):
        """Internal thread target: runs the event loop."""
        print("Listening for controller input...")

        for event in self.gamepad.read_loop():
            if not self.running:
                break
            
            print("EVENT:", event)

            # Buttons EV_KEY

            if event.type == ecodes.EV_KEY:
                code = event.code
                value = event.value

                if code == ecodes.BTN_SOUTH:
                    self.callback("button_a", value)
                
                if code == ecodes.BTN_EAST:
                    self.callback("button_b", value)

                # Add more buttons here
                continue
            
            # Analog sticks

            if event.type != ecodes.EV_ABS:
                continue
            absevent = categorize(event)
            code = absevent.event.code
            value = absevent.event.value

            # Left Trigger
            if code == ecodes.ABS_Z:
                self.callback("left_trigger", value)

            # Right Trigger
            if code == ecodes.ABS_RZ:
                self.callback("right_trigger", value)

    def start(self):
        """Start the listener in a background thread."""
        if self.thread is None:
            self.running = True
            self.thread = threading.Thread(target=self._listen, daemon=True)
            self.thread.start()

    def stop(self):
        """Stop the listener thread cleanly."""
        self.running = False