from evdev import InputDevice, categorize, ecodes

# Find the controller path: ls /dev/input/

gamepad = InputDevice('/dev/input/event0') 
print('Listening for controller events.....')

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        print(f"Button: {keyevent.keycode}, State: {keyevent.keystate}")

    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        print(f"Axis: {absevent.event.code}, Value: {absevent.event.value}")


              