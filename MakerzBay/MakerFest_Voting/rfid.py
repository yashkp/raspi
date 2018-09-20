#from settings import *
import time, json, httplib, os, atexit, thread
from evdev import InputDevice, list_devices, categorize, ecodes

KEYCODES = {
	'KEY_0': '0', 'KEY_1': '1', 'KEY_2': '2', 'KEY_3': '3', 'KEY_4': '4', 
	'KEY_5': '5', 'KEY_6': '6', 'KEY_7': '7', 'KEY_8': '8', 'KEY_9': '9'
}

def get_scanner_device():
    devices = map(InputDevice, list_devices())
    device = None
    for dev in devices:
        if dev.name == 'RFIDeas USB Keyboard':
            device = dev
            break
    return device

def init(device):
    print 'hello'
    atexit.register(cleanup, device)

    device.grab()

def cleanup(device):
	device.ungrab()

def log(badgenum):
        print badgenum

def get_input(device):
	val = ''
	for event in device.read_loop():
		ev = categorize(event)
		if event.type == ecodes.EV_KEY and ev.keystate == ev.key_down:
			if ev.keycode == 'KEY_ENTER':
				break
			val += KEYCODES[ev.keycode]
	return val

def initialize_from_voting():
    global val1
    global device
    val1 = 4
    device = get_scanner_device()
    
    if(str(device) == 'None'):
        print 'Device Not Found'

    init(device)
    return device

def summ(val2):
    global val1
    return val1+val2

global val1
global device

if __name__ == "__main__":
    global val1
    val1 = 5
    print 'hello'
    
    device = get_scanner_device()
    if str(device) == 'None':
        print "Device not found! Exiting!"

    init(device)
    while True:
        print 'hey there'
        try: 
            badgenum = int(get_input(device))
            print 'found'
            thread.start_new_thread(log, (badgenum,))
                                
        except ValueError:
            time.sleep(0.1)
