import RPi.GPIO as io
from azure.servicebus import ServiceBusService, Message, Queue
io.setmode(io.BCM)

in1_pin = 5
in2_pin = 6

in3_pin = 20
in4_pin = 21

io.setup(in1_pin, io.OUT)
io.setup(in2_pin, io.OUT)
io.setup(in3_pin, io.OUT)
io.setup(in4_pin, io.OUT)

bus_service = ServiceBusService(service_namespace='debrisbot-ns',
    shared_access_key_name='RootManageSharedAccessKey',
    shared_access_key_value='QPxUGbIzO33d5oeTjv3NRPe+DLkzP+f+lPwwken6K00=')

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

def getCommand():
    msg = bus_service.receive_queue_message('botqueue', peek_lock=False)
    msg = msg.body
    print msg
    if(msg is not None):
        msg = msg.split(' ')[1]
        return msg

#front()

while True:
    cmd = getCommand()
    direction = cmd
    print direction
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
io.cleanup()
