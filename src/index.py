import json
import bz2
import os

from pathlib import Path
import re

import saveLocationCountryJson
import probesDataParse
import rootAParse
import rootKParse

filePath = '../probesData/20220824.json'

metricsFilePaths = ['../metrics/Medição 1 A IPV4.json', '../metrics/Medição 3 A IPV6.json']

path = Path(__file__).parent / str(filePath)

# CRUZAR DADOS DO ARQUIVO DE PROBES E DO ARQUIVO DE MÉTRICAS

# PORCENTAGEM DE PROBES SE CONECTAM AO MESMO PAÍS DE ORIGEM

# PORCENTAGEM DE PROBES QUE SE CONECTAM EM PAÍSES DIFERENTES EM IPV4 E IPV6

# PORCENTAGEM DE PROBES QUE SE CONECTAM AO MESMO PAÍS DE ORIGEM EM UM PROTOCOLO E EM OUTRO NÃO

with path.open() as f:

    data = json.load(f)
    
    probeIdProbeOriginDict = probesDataParse.parseProbesData(data)
    
    print(probeIdProbeOriginDict)
    
    print(data['meta'])
    
    totalProbesCount = data['meta']['total_count']
    
    print(totalProbesCount)
    
    for metricsFilePath in metricsFilePaths :

        probeIdOriginResponses = rootAParse.parseMetrics(metricsFilePath)

        # path = Path(__file__).parent / str(filePath)
        
########### ROOT K


filePath = '../probesData/20220824.json'

metricsFilePaths = ['../metrics/Medição 5 K IPV4.json', 
                    '../metrics/Medição 7 K IPV6.json'
                    ]

path = Path(__file__).parent / str(filePath)

# CRUZAR DADOS DO ARQUIVO DE PROBES E DO ARQUIVO DE MÉTRICAS

# 1 - OK
# PORCENTAGEM DE PROBES SE CONECTAM AO MESMO PAÍS DE ORIGEM

# 2 -
# PORCENTAGEM DE PROBES QUE SE CONECTAM EM PAÍSES DIFERENTES EM IPV4 E IPV6

# 3 -
# PORCENTAGEM DE PROBES QUE SE CONECTAM AO MESMO PAÍS DE ORIGEM EM UM PROTOCOLO E EM OUTRO NÃO

# print(probeIdProbeOriginDict)
    
###
# 1 - OK
# PORCENTAGEM DE PROBES SE CONECTAM AO MESMO PAÍS DE ORIGEM
for metricsFilePath in metricsFilePaths :

    with path.open() as f:

        data = json.load(f)
        
        probeIdProbeOriginDict = probesDataParse.parseProbesData(data)

        probeIdWithSameCountryResponsePercentage = 0
        
        probeIdWithSameCountryResponsePercentage = 0

        probeIdWithSameCountryResponseCount = 0
        
        probeIdWithAlwaysSameCountryResponseCount = 0

        probeIdCountryResponseIPV4 = rootKParse.parseMetrics(metricsFilePath)

        totalActiveProbesIPV4 = len(probeIdCountryResponseIPV4)
        
        percentageOfActiveProbes = 0
        
        print('Total probes: ' + str(len(probeIdProbeOriginDict)))
        
        print('Total active probes: ' + str(totalActiveProbesIPV4))
        
        for probeKey in probeIdCountryResponseIPV4 :
            
            alreadyCalculatedProbeId = 0
            
            probeCountryResponses = probeIdCountryResponseIPV4[probeKey]
            
            # ALWAYS FROM SAME ORIGIN COUNTER
            countAlwaysInSameCountryFromOrigin = 0
            
            count = 0
            
            for country in probeCountryResponses :
            
                # JUST COUNT FIRST 2 RESPONSES    
                if ( str(probeKey) in probeIdProbeOriginDict and count < 2 ) :
                    
                    count+=1
                        
                    if ( probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and alreadyCalculatedProbeId < 1 ) :    
                    
                        probeIdWithSameCountryResponseCount += 1
                        
                        alreadyCalculatedProbeId = 1
                        
                    if ( probeIdProbeOriginDict[str(probeKey)] == str(country).upper() ) :
                        
                        countAlwaysInSameCountryFromOrigin += 1
                        
                    # ALWAYS FROM SAME ORIGIN ( 2 responses from same origin of the request )
                    if ( probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and countAlwaysInSameCountryFromOrigin > 1 ) : 
                        
                        probeIdWithAlwaysSameCountryResponseCount += 1
        
            
        probeIdWithSameCountryResponsePercentage = probeIdWithSameCountryResponseCount * 100 / totalActiveProbesIPV4 if probeIdWithSameCountryResponseCount > 0 else 0

        probeIdWithAlwaysSameCountryResponsePercentage = probeIdWithAlwaysSameCountryResponseCount * 100 / totalActiveProbesIPV4 if probeIdWithAlwaysSameCountryResponseCount > 0 else 0

        print(probeIdWithSameCountryResponseCount)
        
        print( probeIdWithSameCountryResponsePercentage )
        
        print( 'Probes with always same origin response: ' + str(probeIdWithAlwaysSameCountryResponsePercentage) )
                    

### 2 
        
# PORCENTAGEM DE PROBES QUE SE CONECTAM EM PAÍSES DIFERENTES EM IPV4 E IPV6

probeIdsWithDifferentCountryResponsePercentage = 0

probeIdsWithSameCountryResponsePercentage = 0

probeIdsWithDifferentCountryResponseCount = 0

probeIdsWithSameCountryResponsseCount = 0

probeIdCountryResponseIPV4 = {}

probeIdCountryResponseIPV6 = {}

totalActiveProbesIPV4 = 0

totalActiveProbesIPV6 = 0

for metricsFilePath in metricsFilePaths :

    with path.open() as f:

        data = json.load(f)
        
        probeIdProbeOriginDict = probesDataParse.parseProbesData(data)

        probeIdWithSameCountryResponsePercentage = 0
        
        probeIdWithSameCountryResponsePercentage = 0

        probeIdWithSameCountryResponseCount = 0
        
        probeIdWithAlwaysSameCountryResponseCount = 0

        if ( str(metricsFilePath).__contains__('IPV4') ) :

            probeIdCountryResponseIPV4 = rootKParse.parseMetrics(metricsFilePath)

            totalActiveProbesIPV4 = len(probeIdCountryResponseIPV4)
            
            percentageOfActiveProbes = 0
            
            print('Total probes: ' + str(len(probeIdProbeOriginDict)))
            
            print('Total active probes: ' + str(totalActiveProbesIPV4))

        else :
            
            probeIdCountryResponseIPV6 = rootKParse.parseMetrics(metricsFilePath)

            totalActiveProbesIPV6 = len(probeIdCountryResponseIPV6)
            
            percentageOfActiveProbes = 0
            
            print('Total probes: ' + str(len(probeIdProbeOriginDict)))
            
            print('Total active probes: ' + str(totalActiveProbesIPV6))
        
saveLocationCountryJson.compareLocationsFromRootAWithLocationsFromRootK()
    
# for probeKey in probeIdCountryResponseIPV4 :
    
#     alreadyCalculatedProbeId = 0
    
#     probeCountryResponses = probeIdCountryResponseIPV4[probeKey]
    
#     # ALWAYS FROM SAME ORIGIN COUNTER
#     countAlwaysInSameCountryFromOrigin = 0
    
#     count = 0
    
#     for country in probeCountryResponses :
    