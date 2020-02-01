import time as t
import os
import datetime 


while 1:
    #take a poll of data and store it in currentData.json
    os.system('python3 storeAndWriteCurrentData.py')
    t.sleep(0.25)
    now = datetime.datetime.now()
    #append the data to previous datafile
    os.system('python3 updateData.py')
    print('last took data on ' +str(now.month) + "/" + str(now.day) + "/" +str(now.year) + " at " + str(now.hour) + ":" + str(now.minute))
    t.sleep(3600)
    


