import os
import RPi.GPIO as io
import json
import datetime as dt
import writeGrowBoxDates as writeDate
import relay
import time
import sendEmail

#######################################################################################
#Constants
#######################################################################################
#variable for who the notifications for the growbox should be sent to
emailRecipients = "just me"
timeOfGrowth = 2 # of weeks the mushrooms will sit in the
cycleStatus = "cycleStatus" #this is added to the full data to indicate if the mushrooms are done or not

#######################################################################################
#pin setup
#######################################################################################
startButtonPin       = 27
waterEmptyPin        = 25
waterFullPin         = 6
redLEDPin            = 20 # on if temperature out of range
blueLEDPin           = 19 # on if humidity water level low
yellowLEDPin         = 21 # on if humidity out of range
greenLEDPin          = 13 # on while grow cycle is in action
THSensorLCDPin       = 24
THSensorWebsitePin   = 23
humidifierControlPin = 22
sunlightPin          = 5

#######################################################################################
#Setup GPIO
#######################################################################################
io.setwarnings(False)
io.setmode(io.BCM)
io.setup(waterEmptyPin, io.IN, pull_up_down=io.PUD_DOWN)
io.setup(waterFullPin,  io.IN, pull_up_down=io.PUD_DOWN)

#######################################################################################
#Function Definitions
#######################################################################################
#function to notify user that the mushroom humidifier needs to be refilled
def waterIsLow(channel):
    #Turn Blue indicator LED on
    relay.relayOnOff(blueLEDPin, "on")
    
    message = """
    Subject: Mushroom Water level is Low
    The Digital water level sensor was triggered, Refill the mushroom humidifier water.
    """

    #send email
    sendEmail.sendEmail(emailRecipients, message)

#function to turn off blue indicator LED
def waterIsHigh(channel):
    relay.relayOnOff(blueLEDPin, "off")

#######################################################################################
#Setup Interrupt pins
#######################################################################################
#Setup interrupt for digital water level sensor    
io.add_event_detect(waterEmptyPin, io.RISING, callback=waterIsLow, bouncetime=300)
io.add_event_detect(waterFullPin, io.FALLING, callback=waterIsHigh, bouncetime=300)

#######################################################################################
#store the current date and calculate finished date
#######################################################################################
startDate = dt.datetime.now()
endDate = startDate + dt.timedelta(weeks=timeOfGrowth)
writeDate.addDateToData("startDate", startDate.strftime("%c")) #the strftime("%c") will print as "Tue Apr 30 19:41:43 2019" for example
writeDate.addDateToData("endDate", endDate.strftime("%c")[0:10]) #just using the [0:10] shortens it to "Tue Apr 30"
#write the start and end date to single file (the LCD code will use this so it can read the dates quickly and easily)
dates = {"startDate": startDate.strftime("%c")[0:10], "endDate": endDate.strftime("%c")[0:10], "cycleStatus": "in use"}
with open("dates.json", "w") as outfile:
    json.dump(dates, outfile)

#######################################################################################
#turn on green LED to indicate the grow cycle has started
#and
#tell the data in the website that the mushrooms are currently in the chamber for the three week cycle
#######################################################################################
relay.relayOnOff(greenLEDPin, "on")
writeDate.addDateToData(cycleStatus, "in use") #the website can use this

#######################################################################################
#Continuous loop while mushrooms sit in the chamber (just sunlight LED control)
#######################################################################################
daysPast = 0
while daysPast < 3*7: #until 3 weeks have past, keep turning on and off the sunlight in this loop
    hour = 60*60 #one hour in seconds

    onTime = 18 * hour # on time is 18 hours
    offTime = 6 * hour # off time is 6 hours

    #turn on sunlight (uses inverted logic because of relay)
    relay.relayOnOff(sunlightPin, "off")
    time.sleep(onTime)

    #turn off sunlight (uses inverted logic because of relay)
    relay.relayOnOff(sunlightPin, "on")
    time.sleep(offTime)

    daysPast = daysPast + 1

#######################################################################################
#end of growth cycle, turn stuff off
#######################################################################################
#turn off green LED to indicate the grow cycle is over
relay.relayOnOff(greenLEDPin, "off")

#######################################################################################
#tell the full data file that the mushrooms are not in the fruiting cycle anymore
#######################################################################################
writeDate.addDateToData(cycleStatus, "Done")

#tell that small file that the mushroom grow cycle is over(the LCD code will use this so it can read the dates quickly and easily)
dates["cycleStatus"] = "waiting for next batch" #update the dictionary
with open("dates.json", "w") as outfile:
    json.dump(dates, outfile)

#######################################################################################
#Email the user that the mushies are ready
#######################################################################################
mushroomEmailMessage = """
Subject: Mushrooms Ready
Hey! your mushrooms are ready for harvesting, Come Get em!
"""
    
sendEmail.sendEmail(emailRecipients, mushroomEmailMessage)
    




