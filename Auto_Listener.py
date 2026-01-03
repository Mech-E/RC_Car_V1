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

        try:
            for event in self.gamepad.read_loop():
                if not self.running:
                    break

                # Debug print
                print("EVENT:", event)

                # BUTTONS (EV_KEY)
                if event.type == ecodes.EV_KEY:
                    code = event.code
                    value = event.value

                    if code == ecodes.BTN_SOUTH:
                        self.callback("Button A", value)
                    elif code == ecodes.BTN_EAST:
                        self.callback("Button B", value)
                    elif code == ecodes.BTN_NORTH:
                        self.callback("Button X", value)
                    elif code == ecodes.BTN_WEST:
                        self.callback("Button Y", value)
                    elif code == ecodes.BTN_DPAD_UP:
                        self.callback("DPad Up", value)
                    elif code == ecodes.BTN_DPAD_DOWN:
                        self.callback("DPad Down", value)
                    elif code == ecodes.BTN_DPAD_LEFT:
                        self.callback("DPad Left", value)
                    elif code == ecodes.BTN_DPAD_RIGHT:
                        self.callback("DPad Right", value)
                    elif code == ecodes.BTN_TR:
                        self.callback("Right Bumper", value)
                    elif code == ecodes.BTN_TL:
                        self.callback("Left Bumper", value)
                    elif code == ecodes.BTN_START:
                        self.callback("Start", value)
                    elif code == ecodes.BTN_SELECT:
                        self.callback("Select", value)

                    # Done with EV_KEY
                    continue

                # ANALOG (EV_ABS)
                if event.type == ecodes.EV_ABS:
                    absevent = categorize(event)
                    code = absevent.event.code
                    value = absevent.event.value

                    if code == ecodes.ABS_Z:
                        self.callback("Left Trigger", value)
                    elif code == ecodes.ABS_RZ:
                        self.callback("Right Trigger", value)
                    elif code == ecodes.ABS_X:
                        self.callback("Left Stick Horizontal", value)
                    elif code == ecodes.ABS_Y:
                        self.callback("Left Stick Vertical", value)
                    elif code == ecodes.ABS_RX:
                        self.callback("Right Stick Horizontal", value)
                    elif code == ecodes.ABS_RY:
                        self.callback("Right Stick Vertical", value)

        except OSError:
            print("Controller disconnected")
            self.running = False

    def start(self):
        """Start the listener in a background thread."""
        if self.thread is None:
            self.running = True
            self.thread = threading.Thread(target=self._listen, daemon=True)
            self.thread.start()

    def stop(self):
        """Stop the listener thread cleanly."""
        self.running = False