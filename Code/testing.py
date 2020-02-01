#this file was to test interrupts, i don't think im done with it
import RPi.GPIO as io

startButtonPin = 27

#setup GPIO
io.setwarnings(False)
io.setmode(io.BCM)
io.setup(startButtonPin, io.IN, pull_up_down=io.PUD_DOWN)


def startGrowthCycle(channel):
    
    import relay
    ledpin = 26
    delay = 1
    relay.relayOnOff(ledpin, "on")
    
    
io.add_event_detect(startButtonPin, io.RISING, callback=startGrowthCycle, bouncetime=300)




