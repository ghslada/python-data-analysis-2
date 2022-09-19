import json

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

import probesDataParse
import rootAParse
import rootKParse

def resolveAnswer3() :
    
    print('Resolving answer 3...')
    
    
    # ROOT A 2022

    filePath = '../probesData/20220824.json'

    metricsFilePaths = ['../metrics/Medição 1 A IPV4.json',
                        '../metrics/Medição 3 A IPV6.json']

    path = Path(__file__).parent / str(filePath)

    locationCountriesFilePath = './util/LocationCountries.json'

    locationCountriesPath = Path(__file__).parent / str(locationCountriesFilePath)

    rootAFilePathIndex = 1

    # 3 -
    # PORCENTAGEM DE PROBES QUE SE CONECTAM AO MESMO PAÍS DE ORIGEM EM UM PROTOCOLO E EM OUTRO NÃO

    probeIdCountryResponseIPV4 = {}

    probeIdCountryResponseIPV6 = {}

    totalActiveProbesIPV4 = 0

    totalActiveProbesIPV6 = 0
    
    probeIdProbeOriginDict = {}
    
    rootAFilePathIndex = 1
    
    for metricsFilePath in metricsFilePaths:

        with path.open() as f:

            data = json.load(f)

            probeIdProbeOriginDict = probesDataParse.parseProbesData(data)
            
            if ( str(metricsFilePath).__contains__('IPV4') ) :

                probeIdCountryResponseIPV4 = rootAParse.parseMetrics(metricsFilePath)

                totalActiveProbesIPV4 = len(probeIdCountryResponseIPV4)

                # REPLACE THE VALUES OF THE LOCATION BY THE VALUE OF THE LOCATION COUNTRY
                with locationCountriesPath.open() as lcf:

                    locationCountries = json.loads(lcf.read())

                    for probeId in probeIdCountryResponseIPV4:

                        locationValues = probeIdCountryResponseIPV4[probeId]

                        probeLocationIdx = 0

                        for locationValue in locationValues:

                            if (locationValue in locationCountries):

                                # print('Location in: '+locationValue)
                                probeIdCountryResponseIPV4[probeId][probeLocationIdx] = locationCountries[locationValue]

                            probeLocationIdx += 1
                            
            else :
                
                probeIdCountryResponseIPV6 = rootAParse.parseMetrics(metricsFilePath)

                totalActiveProbesIPV6 = len(probeIdCountryResponseIPV6)

                # REPLACE THE VALUES OF THE LOCATION BY THE VALUE OF THE LOCATION COUNTRY
                with locationCountriesPath.open() as lcf:

                    locationCountries = json.loads(lcf.read())

                    for probeId in probeIdCountryResponseIPV6:

                        locationValues = probeIdCountryResponseIPV6[probeId]

                        probeLocationIdx = 0

                        for locationValue in locationValues:

                            if (locationValue in locationCountries):

                                # print('Location in: '+locationValue)
                                probeIdCountryResponseIPV6[probeId][probeLocationIdx] = locationCountries[locationValue]

                            probeLocationIdx += 1
                            
        # REPLACE END

        percentageOfActiveProbes = 0

        print('Total active probes IPV4: ' + str(totalActiveProbesIPV4))
        print('Total active probes IPV6: ' + str(totalActiveProbesIPV6))

    ###################################################
    # ROOT A IPV4 2022 START

    probeIdWithSameCountryResponsePercentage = 0

    probeIdWithSameCountryResponseCount = 0

    probeIdWithAlwaysSameCountryResponseCount = 0

    alreadyCalculatedProbes = []  

    for probeKey in probeIdCountryResponseIPV4:

        alreadyCalculatedProbeId = 0

        probeCountryResponses = probeIdCountryResponseIPV4[probeKey]

        # ALWAYS FROM SAME ORIGIN COUNTER
        countAlwaysInSameCountryFromOrigin = 0

        count = 0

        for country in probeCountryResponses:

            # print(country)

            # JUST COUNT FIRST 2 RESPONSES
            if (str(probeKey) in probeIdProbeOriginDict and count < 2):

                count += 1

                if ( probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and probeKey not in alreadyCalculatedProbes ):

                    if probeKey in probeIdCountryResponseIPV6 :
                        
                        for countryToCompare in probeIdCountryResponseIPV6[probeKey] :
                            
                            if str(country).upper() == str(countryToCompare).upper() :

                                probeIdWithSameCountryResponseCount += 1
                                            
                                alreadyCalculatedProbes.append(probeKey)
        
    print(str(probeIdWithSameCountryResponseCount) + ' of ' + str(totalActiveProbesIPV4) + ' IPV4 probe IDs received responses from same country origin of request in IPV4 and IPV6')
                                
    probeIdWithSameCountryResponsePercentage = probeIdWithSameCountryResponseCount * 100 / totalActiveProbesIPV4
    
    probeIdWithNoResponsesFromSameCountryResponsePercentage = 100 - probeIdWithSameCountryResponsePercentage
    
    probeWithSameCountryMessage = 'Porcentagem de probes do protocolo IPV4 com respostas do mesmo país onde estão localizadas no protocolo IPV4 e IPV6 '
    
    print(probeWithSameCountryMessage+str(probeIdWithSameCountryResponsePercentage))
                            
    var022 = [probeIdWithSameCountryResponsePercentage, probeIdWithNoResponsesFromSameCountryResponsePercentage]

    yearOfMeasurement = '2022'
    
    if (rootAFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV4 que receberam pelo menos uma resposta do mesmo país onde estão localizadas em ambos os protocolos IPV4 e IPV6', 'Probes do protocolo IPV4 que não receberam nenhuma resposta do mesmo país onde estão localizadas em ambos os protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(28, 24), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
    metricsFilePath = '../metrics/Medição 1 A IPV4.json'
    
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '3 - ' + metricsFilePath + ' 2022.png')

    rootAFilePathIndex += 1
                    
    # ROOT A IPV4 2022 END
    
    
    ###################################################
    # ROOT A IPV6 2022 START

    probeIdWithSameCountryResponsePercentage = 0

    probeIdWithSameCountryResponseCount = 0

    probeIdWithAlwaysSameCountryResponseCount = 0

    alreadyCalculatedProbes = []  

    for probeKey in probeIdCountryResponseIPV6:

        alreadyCalculatedProbeId = 0

        probeCountryResponses = probeIdCountryResponseIPV6[probeKey]

        # ALWAYS FROM SAME ORIGIN COUNTER
        countAlwaysInSameCountryFromOrigin = 0

        count = 0

        for country in probeCountryResponses:

            # print(country)

            # JUST COUNT FIRST 2 RESPONSES
            if (str(probeKey) in probeIdProbeOriginDict and count < 2):

                count += 1

                if ( probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and probeKey not in alreadyCalculatedProbes ):

                    if probeKey in probeIdCountryResponseIPV4 :
                        
                        for countryToCompare in probeIdCountryResponseIPV4[probeKey] :
                            
                            if str(country).upper() == str(countryToCompare).upper() :

                                probeIdWithSameCountryResponseCount += 1
                                            
                                alreadyCalculatedProbes.append(probeKey)
        
    print(str(probeIdWithSameCountryResponseCount) + ' of ' + str(totalActiveProbesIPV6) + ' IPV6 probe IDs received responses from same country origin of request in IPV4 and IPV6')
                                
    probeIdWithSameCountryResponsePercentage = probeIdWithSameCountryResponseCount * 100 / totalActiveProbesIPV6
    
    probeIdWithNoResponsesFromSameCountryResponsePercentage = 100 - probeIdWithSameCountryResponsePercentage
    
    probeWithSameCountryMessage = 'Porcentagem de probes do protocolo IPV6 com respostas do mesmo país onde estão localizadas no protocolo IPV4 e IPV6 '
    
    print(probeWithSameCountryMessage+str(probeIdWithSameCountryResponsePercentage))
                            
    var022 = [probeIdWithSameCountryResponsePercentage, probeIdWithNoResponsesFromSameCountryResponsePercentage]

    yearOfMeasurement = '2022'
    
    if (rootAFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV6 que receberam pelo menos uma resposta do mesmo país onde estão localizadas em ambos os protocolos IPV4 e IPV6', 'Probes do protocolo IPV6 que não receberam nenhuma resposta do mesmo país onde estão localizadas em ambos os protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(39, 26), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
    metricsFilePath = '../metrics/Medição 3 A IPV6.json'
    
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '3 - ' + metricsFilePath + ' 2022.png')

    rootAFilePathIndex += 1
                    
    # ROOT A IPV6 2022 END


    ############################################################################################
    # ROOT A 2017

    filePath = '../probesData/20170824.json'

    metricsFilePaths = ['../metrics/Medição 2 A IPV4.json',
                        '../metrics/Medição 4 A IPV6.json']

    path = Path(__file__).parent / str(filePath)

    locationCountriesFilePath = './util/LocationCountries.json'

    locationCountriesPath = Path(__file__).parent / str(locationCountriesFilePath)

    rootAFilePathIndex = 1

    # 3 -
    # PORCENTAGEM DE PROBES QUE SE CONECTAM AO MESMO PAÍS DE ORIGEM EM UM PROTOCOLO E EM OUTRO NÃO

    probeIdCountryResponseIPV4 = {}

    probeIdCountryResponseIPV6 = {}

    totalActiveProbesIPV4 = 0

    totalActiveProbesIPV6 = 0
    
    probeIdProbeOriginDict = {}
    
    rootAFilePathIndex = 1
    
    for metricsFilePath in metricsFilePaths:

        with path.open() as f:

            data = json.load(f)

            probeIdProbeOriginDict = probesDataParse.parseProbesData(data)
            
            if ( str(metricsFilePath).__contains__('IPV4') ) :

                probeIdCountryResponseIPV4 = rootAParse.parseMetrics(metricsFilePath)

                totalActiveProbesIPV4 = len(probeIdCountryResponseIPV4)

                # REPLACE THE VALUES OF THE LOCATION BY THE VALUE OF THE LOCATION COUNTRY
                with locationCountriesPath.open() as lcf:

                    locationCountries = json.loads(lcf.read())

                    for probeId in probeIdCountryResponseIPV4:

                        locationValues = probeIdCountryResponseIPV4[probeId]

                        probeLocationIdx = 0

                        for locationValue in locationValues:

                            if (locationValue in locationCountries):

                                # print('Location in: '+locationValue)
                                probeIdCountryResponseIPV4[probeId][probeLocationIdx] = locationCountries[locationValue]

                            probeLocationIdx += 1
                            
            else :
                
                probeIdCountryResponseIPV6 = rootAParse.parseMetrics(metricsFilePath)

                totalActiveProbesIPV6 = len(probeIdCountryResponseIPV6)

                # REPLACE THE VALUES OF THE LOCATION BY THE VALUE OF THE LOCATION COUNTRY
                with locationCountriesPath.open() as lcf:

                    locationCountries = json.loads(lcf.read())

                    for probeId in probeIdCountryResponseIPV6:

                        locationValues = probeIdCountryResponseIPV6[probeId]

                        probeLocationIdx = 0

                        for locationValue in locationValues:

                            if (locationValue in locationCountries):

                                # print('Location in: '+locationValue)
                                probeIdCountryResponseIPV6[probeId][probeLocationIdx] = locationCountries[locationValue]

                            probeLocationIdx += 1
                            
        # REPLACE END

        percentageOfActiveProbes = 0

        print('Total active probes IPV4: ' + str(totalActiveProbesIPV4))
        print('Total active probes IPV6: ' + str(totalActiveProbesIPV6))

    ###################################################
    # ROOT A IPV4 2022 START

    probeIdWithSameCountryResponsePercentage = 0

    probeIdWithSameCountryResponseCount = 0

    probeIdWithAlwaysSameCountryResponseCount = 0

    alreadyCalculatedProbes = []  

    for probeKey in probeIdCountryResponseIPV4:

        alreadyCalculatedProbeId = 0

        probeCountryResponses = probeIdCountryResponseIPV4[probeKey]

        # ALWAYS FROM SAME ORIGIN COUNTER
        countAlwaysInSameCountryFromOrigin = 0

        count = 0

        for country in probeCountryResponses:

            # print(country)

            # JUST COUNT FIRST 2 RESPONSES
            if (str(probeKey) in probeIdProbeOriginDict and count < 2):

                count += 1

                if ( probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and probeKey not in alreadyCalculatedProbes ):

                    if probeKey in probeIdCountryResponseIPV6 :
                        
                        for countryToCompare in probeIdCountryResponseIPV6[probeKey] :
                            
                            if str(country).upper() == str(countryToCompare).upper() :

                                probeIdWithSameCountryResponseCount += 1
                                            
                                alreadyCalculatedProbes.append(probeKey)
        
    print(str(probeIdWithSameCountryResponseCount) + ' of ' + str(totalActiveProbesIPV4) + ' IPV4 probe IDs received responses from same country origin of request in IPV4 and IPV6')
                                
    probeIdWithSameCountryResponsePercentage = probeIdWithSameCountryResponseCount * 100 / totalActiveProbesIPV4
    
    probeIdWithNoResponsesFromSameCountryResponsePercentage = 100 - probeIdWithSameCountryResponsePercentage
    
    probeWithSameCountryMessage = 'Porcentagem de probes do protocolo IPV4 com respostas do mesmo país onde estão localizadas no protocolo IPV4 e IPV6 '
    
    print(probeWithSameCountryMessage+str(probeIdWithSameCountryResponsePercentage))
                            
    var022 = [probeIdWithSameCountryResponsePercentage, probeIdWithNoResponsesFromSameCountryResponsePercentage]

    yearOfMeasurement = '2017'
    
    if (rootAFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV4 que receberam pelo menos uma resposta do mesmo país onde estão localizadas em ambos os protocolos IPV4 e IPV6', 'Probes do protocolo IPV4 que não receberam nenhuma resposta do mesmo país onde estão localizadas em ambos os protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(36, 26), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
    metricsFilePath = '../metrics/Medição 2 A IPV4.json'
    
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '3 - ' + metricsFilePath + ' 2017.png')

    rootAFilePathIndex += 1
                    
    # ROOT A IPV4 2022 END
    
    
    ###################################################
    # ROOT A IPV6 2022 START

    probeIdWithSameCountryResponsePercentage = 0

    probeIdWithSameCountryResponseCount = 0

    probeIdWithAlwaysSameCountryResponseCount = 0

    alreadyCalculatedProbes = []  

    for probeKey in probeIdCountryResponseIPV6:

        alreadyCalculatedProbeId = 0

        probeCountryResponses = probeIdCountryResponseIPV6[probeKey]

        # ALWAYS FROM SAME ORIGIN COUNTER
        countAlwaysInSameCountryFromOrigin = 0

        count = 0

        for country in probeCountryResponses:

            # print(country)

            # JUST COUNT FIRST 2 RESPONSES
            if (str(probeKey) in probeIdProbeOriginDict and count < 2):

                count += 1

                if ( probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and probeKey not in alreadyCalculatedProbes ):

                    if probeKey in probeIdCountryResponseIPV4 :
                        
                        for countryToCompare in probeIdCountryResponseIPV4[probeKey] :
                            
                            if str(country).upper() == str(countryToCompare).upper() :

                                probeIdWithSameCountryResponseCount += 1
                                            
                                alreadyCalculatedProbes.append(probeKey)
        
    print(str(probeIdWithSameCountryResponseCount) + ' of ' + str(totalActiveProbesIPV6) + ' IPV6 probe IDs received responses from same country origin of request in IPV4 and IPV6')
                                
    probeIdWithSameCountryResponsePercentage = probeIdWithSameCountryResponseCount * 100 / totalActiveProbesIPV6
    
    probeIdWithNoResponsesFromSameCountryResponsePercentage = 100 - probeIdWithSameCountryResponsePercentage
    
    probeWithSameCountryMessage = 'Porcentagem de probes do protocolo IPV6 com respostas do mesmo país onde estão localizadas no protocolo IPV4 e IPV6 '
    
    print(probeWithSameCountryMessage+str(probeIdWithSameCountryResponsePercentage))
                            
    var022 = [probeIdWithSameCountryResponsePercentage, probeIdWithNoResponsesFromSameCountryResponsePercentage]

    yearOfMeasurement = '2017'
    
    if (rootAFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV6 que receberam pelo menos uma resposta do mesmo país onde estão localizadas em ambos os protocolos IPV4 e IPV6', 'Probes do protocolo IPV6 que não receberam nenhuma resposta do mesmo país onde estão localizadas em ambos os protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(36, 26), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
    metricsFilePath = '../metrics/Medição 4 A IPV6.json'
    
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '3 - ' + metricsFilePath + ' 2017.png')

    rootAFilePathIndex += 1
                    
    # ROOT A IPV6 2022 END
