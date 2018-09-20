import RPi.GPIO as io
io.setmode(io.BCM)

cPin = 14

io.setup(cPin, io.OUT)    


while True:
    cmd = raw_input("Command, f/r 0..9, E.g. f5 :")
    direction = cmd[0]
    if direction == "0":
        io.output(cPin, False)
        print direction
    elif direction == "1":
        io.output(cPin, True)
        print direction

io.cleanup()
