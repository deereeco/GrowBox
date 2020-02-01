def addDateToData(nameOfData, dateToWrite):
    import json
    
    #read the current list of data already stored
    with open('updatedData.json','r') as fullDataFile:
        fullData = json.load(fullDataFile)

        fullDataFile.close()

    #add date to the dictionary
    fullData[nameOfData] = dateToWrite

    #rewrite the data with the updated stuff
    with open('updatedData.json', 'w') as fullDataFile:
        json.dump(fullData, fullDataFile)
        fullDataFile.close()
        
        
        
        
        
        