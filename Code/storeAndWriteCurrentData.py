import DHT22 as dht
import json
import datetime

#polling from the sensor
THSensorWebsitePin   = 23
humidity, temperature = dht.humidityAndTempCheck(THSensorWebsitePin) 

#make a time stamp for the data just captured
now = datetime.datetime.now()

#put data and timestamp into object
data = {
    "temperature": [temperature],
    "humidity": [humidity],
    "time": {
        "year": [now.year],
        "month": [now.month],
        "day": [now.day],
        "hour": [now.hour],
        "minute": [now.minute]
    }
}

with open("currentData.json", "w") as outfile:
    json.dump(data, outfile)





