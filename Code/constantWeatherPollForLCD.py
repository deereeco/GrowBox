import lcd_i2c as lcd
import json
import DHT22 as dht
import datetime as dt
import sendEmail
import time
import relay

#######################################################################################
#Constants
#######################################################################################
delay = 2 # in seconds
tempMin = 60
tempMax = 80
emailRecipients = "just me"

#######################################################################################
#Pin setup
#######################################################################################
redLEDPin            = 20 # on if temperature out of range
THSensorLCDPin       = 24

def LCDLinesDuringGrowCycle(humidity,temperature, dates):
        
    line1 = "Strt: " + dates["startDate"]
    line2 = "End: " + dates["endDate"]
    line3 = "Temp: " + str(temperature)[:2] + " F"
    line4 = "Humidity: " + str(humidity)[:2] + " %"

    lcd.postToLCD(line1, line2, line3, line4)
    
def LCDLinesNotDuringGrowCycle(humidity,temperature, dates):

    line1 = "Last Cycle Ended"
    line2 = "on: " + dates["endDate"]
    line3 = "Temp: " + str(temperature)[:2] + " F"
    line4 = "Humidity: " + str(humidity)[:2] + " %"
    
    lcd.postToLCD(line1, line2, line3, line4)

#######################################################################################
#start the infinite loop
#######################################################################################
startTime = time.time()
while 1:

    #take a temp measurement with the LCD temp/humidifier sensor
    humidity, temperature = dht.humidityAndTempCheck(THSensorLCDPin)

    #get the dates for growth cycle
    with open("dates.json", "r") as file:
        dates = json.load(file)
        file.close()

    #if the growth cycle is taking place, display this to the LCD screen
    if dates["cycleStatus"].lower() == "in use": 
        LCDLinesDuringGrowCycle(humidity,temperature, dates)

    #if the growth cycle is taking place, display this to the LCD screen
    elif dates["cycleStatus"].lower() == "waiting for next batch":
        LCDLinesNotDuringGrowCycle(humidity,temperature, dates)




    #if the temp is out of range
    if temperature > tempMax or temperature < tempMin:

        #turn on the red indicator (warning) LED
        relay.relayOnOff(redLEDPin, "on")

        #check how long its been out of range in seconds
        timeOutOfRange = time.time() - startTime

        #if its been out of range for an hour...
        if timeOutOfRange > 3600:

            message ="""
            Subject: Temperature Out Of Range
            The mushroom chamber temperature has been out of range for an hour
            """ + "The current temperature is: " + str(temperature) + " F"

            #send email                        
            sendEmail.sendEmail(emailRecipients, message)

            #update the start time to restart the hour timer
            startTime = time.time()

    #if its in range...
    else:
        #turn off the red indicator (warning) LED
        relay.relayOnOff(redLEDPin, "off")

        #update the start time to restart the hour timer (see out of range case above about the email)
        startTime = time.time()

    #go to sleep before next time the loop runs
    time.sleep(delay)
        







