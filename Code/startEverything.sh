# this is a script to start all the programs for the growbox
# this can be used for the COEIT celebration

# go to the right directory
cd /home/pi/Desktop

# turn off sunlight for presentation
python3 turnOffSunlight.py &

# this is the script for the start button to start the "startGrowthCycle"
python3 BUTTONstartEverything.py &

# this starts the humidity controller
python3 humidityBangBangController.py &

# this starts the constant LCD refresh with the sensor data
python3 constantWeatherPollForLCD.py & 

# this starts the hourly Temp and humidity for the wesite data
python3 hourlyWeatherPollAndDataUpdate.py &

# stop node servers running and start the data server locally
pkill -9 node
node myDataServer.js &
 



