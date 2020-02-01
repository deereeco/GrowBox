import time as t
import os
import datetime
import RPi.GPIO as io

#######################################################################################
#pin setup
#######################################################################################
startButtonPin       = 27

#######################################################################################
#Setup GPIO
#######################################################################################
io.setwarnings(False)
io.setmode(io.BCM)
io.setup(startButtonPin, io.IN, pull_up_down=io.PUD_DOWN)

while 1:
    
    if io.input(startButtonPin) == 1:
        #if the button is pressed, start the growth cycle
        os.system('python3 startGrowthCycle.py')

    #if not dont do anything
    t.sleep(0.25)
       












