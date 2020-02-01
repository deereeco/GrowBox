
#pin is the GPIO number
#command is either 'on' or 'off' (caps do not matter)

def relayOnOff(pin, command):

    import RPi.GPIO as io

    #setup GPIO
    io.setwarnings(False)
    io.setmode(io.BCM)
    io.setup(pin, io.OUT)

    '''
    Note the reverse logic for on=low and off=high
    this is just the way the relay is connected
    '''
    if command.lower() == 'off':
        io.output(pin, io.LOW)

    elif command.lower() == 'on':
        io.output(pin, io.HIGH)

    else:
        print("umm, your input arguments are incorrect in someway\n")
        print("you typed: " + command)
        print("the use of this function is relayOnOff(pin, command)")
        print("The only acceptable commands are \'on\' or \'off\'")
        
        
def relayToggle(pin, delay):

    try:
        import RPi.GPIO as io
        import time

        #setup GPIO
        io.setwarnings(False)
        io.setmode(io.BCM)
        io.setup(pin, io.OUT)

        #toggle the relay pin
        io.output(pin, io.LOW)
        time.sleep(delay)
        io.output(pin, io.HIGH)

    except:
        print("An error occured in relayToggle()")


