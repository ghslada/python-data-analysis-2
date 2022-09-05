
    
from os import remove
import re
from ast import For
import pandas as pd
import matplotlib.pyplot as plt
import json
import rootKParse
import saveLocationCountryJson
from pathlib import Path
import re


def saveLocationsFromRootA(data) :
    
    filePath = './util/LocationsFromRootA.json'
    
    my_path = str(Path(__file__).parent) # Figures out the absolute path for you in case your working directory moves around.

    my_path += '\\' + filePath.replace('/', '\\')
    
    jsonData = {}

    try :
    
        with open(my_path, 'r', encoding='utf-8') as f:

            jsonData = json.loads(f.read())

    except :

        print('JSON ainda não foi criado')

    with open(my_path, 'w', encoding='utf-8') as f:

            for key in jsonData.keys() :
                
                if key not in data :
                    
                    data[key] = jsonData[key]
                    
                    print('EXISTING KEY NOT IN NEW DATA: '+key)
                    
                    # exit()
        
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    

def save(data) :
    
    filePath = './util/LocationCountries.json'
    
    my_path = str(Path(__file__).parent) # Figures out the absolute path for you in case your working directory moves around.

    my_path += '\\' + filePath.replace('/', '\\')
    
    jsonData = {}

    try :
    
        with open(my_path, 'r', encoding='utf-8') as f:

            jsonData = json.loads(f.read())

    except :

        print('JSON ainda não foi criado')

    with open(my_path, 'w', encoding='utf-8') as f:

            for key in jsonData.keys() :
                
                if key not in data :
                    
                    data[key] = jsonData[key]
                    
                    print('EXISTING KEY NOT IN NEW DATA: '+key)
                    
                    # exit()
        
            json.dump(data, f, ensure_ascii=False, indent=4)

def compareLocationsFromRootAWithLocationsFromRootK() :
    
    filePath = './util/LocationsComparison.json'
    
    filePathsToCompare = ['./util/LocationCountries.json', './util/LocationsFromRootA.json']
   
    rootKJsonData = {}
    
    rootAJsonData = {}
    
    count = 0

    for filePathToCompare in filePathsToCompare :
            
        my_path = str(Path(__file__).parent) # Figures out the absolute path for you in case your working directory moves around.

        my_path += '\\' + filePathToCompare.replace('/', '\\')
            
        if count == 0 :

            try :
            
                with open(my_path, 'r', encoding='utf-8') as f:

                    rootKJsonData = json.loads(f.read())

            except :

                print('JSON ainda não foi criado')
        
        else :
            
            try :
            
                with open(my_path, 'r', encoding='utf-8') as f:

                    rootAJsonData = json.loads(f.read())

            except :

                print('JSON ainda não foi criado')
    
        count += 1
    
    notInRootKLocationsList = []
        
    InRootKLocationsList = []
        
    for rootAKey in rootAJsonData :        
        
        if rootAKey not in rootKJsonData :   
            
            notInRootKLocationsList.append(rootAKey)
            
        else :
            
            InRootKLocationsList.append(rootAKey)
            
    comparisonData = {}
    
    comparisonData['NOT in RootK locations list'] = notInRootKLocationsList
    print( json.dumps(comparisonData, indent=4))        
            
            
    comparisonData['IN RootK locations list'] = InRootKLocationsList
    print( json.dumps(comparisonData, indent=4))        
            
                
    my_path = str(Path(__file__).parent) # Figures out the absolute path for you in case your working directory moves around.

    my_path += '\\' + filePath.replace('/', '\\')
    # count += 1
    with open(my_path, 'w', encoding='utf-8') as f:

        # rootKJsonData = json.loads(f.read())
        
        json.dump(comparisonData, f, ensure_ascii=False, indent=4)
        

# saveLocationCountryJson.compareLocationsFromRootAWithLocationsFromRootK()
