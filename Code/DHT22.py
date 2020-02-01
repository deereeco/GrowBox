def humidityAndTempCheck(pin):

    import Adafruit_DHT as dht

    sensor = dht.DHT22  
    humidity, temperature = dht.read_retry(sensor, pin)
    if type(temperature) == float:
        temperature = temperature*1.8 + 32 #convert celcius to F
    
    else:
        temperature = 0
        humidity = 0
    

    return(humidity, temperature)
    

    
    
