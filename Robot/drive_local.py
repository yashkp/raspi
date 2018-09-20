import RPi.GPIO as io
io.setmode(io.BCM)

in1_pin = 3
in2_pin = 2

in3_pin = 27
in4_pin = 17

io.setup(in1_pin, io.OUT)
io.setup(in2_pin, io.OUT)
io.setup(in3_pin, io.OUT)
io.setup(in4_pin, io.OUT)

'''
def set(property, value):
    try:
        f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
        f.write(value)
        f.close()	
    except:
        print("Error writing to: " + property + " value: " + value)
 
set("delayed", "0")
set("mode", "pwm")
set("frequency", "500")
set("active", "1")
'''

def front():
    io.output(in1_pin, True)    
    io.output(in2_pin, False)
    io.output(in3_pin, True)    
    io.output(in4_pin, False)
    
def back():
    io.output(in1_pin, False)    
    io.output(in2_pin, True)
    io.output(in3_pin, False)    
    io.output(in4_pin, True)
    
def right():
    io.output(in1_pin, True)    
    io.output(in2_pin, False)
    io.output(in3_pin, False)    
    io.output(in4_pin, False)

def left():
    io.output(in1_pin, False)    
    io.output(in2_pin, False)
    io.output(in3_pin, True)    
    io.output(in4_pin, False)

def stop():
    io.output(in1_pin, False)    
    io.output(in2_pin, False)
    io.output(in3_pin, False)    
    io.output(in4_pin, False)


front()

while True:
    cmd = raw_input("Command, f/r 0..9, E.g. f5 :")
    direction = cmd[0]
    if direction == "w":
        front()
    elif direction == "s":
        back()
    elif direction == "a":
        left()
    elif direction == "d":
        right()
    elif direction == "q": 
        stop()
    elif direction == "e":
        break
    #speed = int(cmd[1]) * 11
    #set("duty", str(speed))
