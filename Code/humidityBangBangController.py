import relay
import sendEmail
import DHT22
import time 

"""
NOTES:

- HUMIDIFIER NEEDS TO START IN THE OFF POSITION

- to turn the humidifier on or off, the relay needs to close AND open to simulate a momentary button push
  this is seen when the relay.relayToggle() is used instead of relay.relayOnOff()
"""

#######################################################################################
#Constants
#######################################################################################
setpointLowBound  = 80; # % relative humidity setpoint
setpointHighBound = 95;
delay = 0.25 #delay of loop in seconds
emailRecipients = "just me"
humidMin = 50 #minimum % relative humidity for notifications

#######################################################################################
#Pin setup
#######################################################################################
humidityInputPin  = 24
humidityOutputPin = 22
yellowLEDPin      = 21 # on if humidity out of range


#take initial measurement
humidity, temperature = DHT22.humidityAndTempCheck(humidityInputPin)

#if the humidity is >= setpoint, wait till it falls below to start the controller
#while humidity >= setpointLowBound:
#    print('waiting for the humidity to drop below setpoint for humidity controller to start')
    
#turn humidifier on
relay.relayToggle(humidityOutputPin, delay)

humidifierOn = True; #if true, humidifier is on, if false, it is off

#######################################################################################
#start the infinite loop
#######################################################################################
startTime = time.time()
while 1:

    #if the humidity is below the setpoint...
    if humidity <= setpointLowBound:
        
        #if the humidifier is already on
        if humidifierOn == True: 
            #don't do anything
            pass 

        #if the humidifier is off
        else:

            #turn it on
            relay.relayToggle(humidityOutputPin, delay)

            #update the variable for the state of the humidifier
            humidifierOn = True
    
    elif humidity >= setpointHighBound:

        #if the humidifier is on
        if humidifierOn == True:

            #turn it off
            relay.relayToggle(humidityOutputPin, delay) 
            #update the variable for the state of the humidifier
            humidifierOn = False

        #if the humidifier is already off
        else: 
            #don't do anything
            pass 

    #rest the Pi
    time.sleep(delay)
    
    #take another measurement
    humidity, temperature = DHT22.humidityAndTempCheck(humidityInputPin)
    
    #if the humidity is out of range
    if humidity < humidMin:

        #turn on the red indicator (warning) LED
        relay.relayOnOff(yellowLEDPin, "on")

        #check how long its been out of range in seconds
        timeOutOfRange = time.time() - startTime

        #if its been out of range for an hour...
        if timeOutOfRange > 3600:

            message ="""
            Subject: Humidity Out Of Range
            The mushroom chamber humidity has been out of range for an hour
            """ + "The current temperature is: " + str(humidity) + " %" 

            #send email                        
            sendEmail.sendEmail(emailRecipients, message)

            #update the start time to restart the hour timer
            startTime = time.time()

    #if its in range...
    else:
        #turn off the red indicator (warning) LED
        relay.relayOnOff(yellowLEDPin, "off")

        #update the start time to restart the hour timer (see out of range case above about the email)
        startTime = time.time()


    
                    
        
    




