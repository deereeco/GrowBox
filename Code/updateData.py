import json

#read the most updated data recorded
with open('currentData.json','r') as currDataFile:
    currData = json.load(currDataFile)
    currDataFile.close()
    
#read the current list of data already stored
with open('updatedData.json','r') as fullDataFile:
    fullData = json.load(fullDataFile)
    fullDataFile.close()

#append the current temp, humidity and the time blocks to the 'updatedData' lists
fullData['temperature'].append(currData['temperature'][0]);
fullData['humidity'].append(currData['humidity'][0]);
fullData['time']['year'].append(currData['time']['year'][0]);
fullData['time']['month'].append(currData['time']['month'][0]);
fullData['time']['day'].append(currData['time']['day'][0]);
fullData['time']['hour'].append(currData['time']['hour'][0]);
fullData['time']['minute'].append(currData['time']['minute'][0]);

#if 60 days have passed, pop old data
if len(fullData['temperature']) >= 60*24:
    fullData['temperature'].pop(0)
    fullData['humidity'].pop(0)
    fullData['time']['year'].pop(0)
    fullData['time']['month'].pop(0)
    fullData['time']['day'].pop(0)
    fullData['time']['hour'].pop(0)
    fullData['time']['minute'].pop(0)
    
#write the updated data to to the file (overwrite)
with open('updatedData.json', 'w') as fullDataFile:
    json.dump(fullData, fullDataFile)
    fullDataFile.close()


