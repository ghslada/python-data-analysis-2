import json
import bz2
import os

from pathlib import Path
import re

import pandas as pd
import matplotlib.pyplot as plt

import saveLocationCountryJson
import probesDataParse
import rootAParse
import rootKParse

    # CRUZAR DADOS DO ARQUIVO DE PROBES E DO ARQUIVO DE MÉTRICAS

    # 1 - K 2022 -> OK, K 2017 -> OK, A 2022 -> OK, A 2017 -> OK
    # PORCENTAGEM DE PROBES SE CONECTAM AO MESMO PAÍS DE ORIGEM

    # 2 -
    # PORCENTAGEM DE PROBES QUE SE CONECTAM EM PAÍSES DIFERENTES EM IPV4 E IPV6

    # 3 -
    # PORCENTAGEM DE PROBES QUE SE CONECTAM AO MESMO PAÍS DE ORIGEM EM UM PROTOCOLO E EM OUTRO NÃO

    # print(probeIdProbeOriginDict)

    # 1 - K - OK
    # PORCENTAGEM DE PROBES SE CONECTAM AO MESMO PAÍS DE ORIGEM


def resolveAnswer1 () :

    # ROOT A 2022

    filePath = '../probesData/20220824.json'

    metricsFilePaths = ['../metrics/Medição 1 A IPV4.json',
                        '../metrics/Medição 3 A IPV6.json']

    path = Path(__file__).parent / str(filePath)

    locationCountriesFilePath = './util/LocationCountries.json'

    locationCountriesPath = Path(__file__).parent / str(locationCountriesFilePath)

    rootAFilePathIndex = 1

    for metricsFilePath in metricsFilePaths:

        with path.open() as f:

            data = json.load(f)

            probeIdProbeOriginDict = probesDataParse.parseProbesData(data)

            probeIdWithSameCountryResponsePercentage = 0

            probeIdWithSameCountryResponsePercentage = 0

            probeIdWithSameCountryResponseCount = 0

            probeIdWithAlwaysSameCountryResponseCount = 0

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

            # REPLACE END

            percentageOfActiveProbes = 0

            print('Total probes: ' + str(len(probeIdProbeOriginDict)))

            print('Total active probes: ' + str(totalActiveProbesIPV4))

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

                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and alreadyCalculatedProbeId < 1):

                            probeIdWithSameCountryResponseCount += 1

                            alreadyCalculatedProbeId = 1

                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper()):

                            countAlwaysInSameCountryFromOrigin += 1

                        # ALWAYS FROM SAME ORIGIN ( 2 responses from same origin of the request )
                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and countAlwaysInSameCountryFromOrigin > 1):

                            probeIdWithAlwaysSameCountryResponseCount += 1

            probeIdWithSameCountryResponsePercentage = probeIdWithSameCountryResponseCount * \
                100 / totalActiveProbesIPV4 if probeIdWithSameCountryResponseCount > 0 else 0

            probeIdWithAlwaysSameCountryResponsePercentage = probeIdWithAlwaysSameCountryResponseCount * \
                100 / totalActiveProbesIPV4 if probeIdWithAlwaysSameCountryResponseCount > 0 else 0

            print(probeIdWithSameCountryResponseCount)

            percentageWithNoResponsesFromSameCountry = 100 - probeIdWithSameCountryResponsePercentage

            # print()
            
            var022 = [probeIdWithSameCountryResponsePercentage, percentageWithNoResponsesFromSameCountry]

            yearOfMeasurement = '2022'

            # if (rootKFilePathIndex % 2 == 0):

            #     yearOfMeasurement = '2022'

            if (rootAFilePathIndex == 2):

                yearOfMeasurement += ' IPV6'

            else:

                yearOfMeasurement += ' IPV4'

            df = pd.DataFrame({
                # '2017': var2017,
                yearOfMeasurement: var022
            }, index=['Probes que receberam resposta do mesmo país onde estão localizadas', 'Probes que não receberam nenhuma resposta do mesmo país onde estão localizadas'])

            ax = df.plot(subplots=True, kind='pie',
                        figsize=(28, 24), autopct='%1.1f%%')

            # plt.figure(figsize=(20, 3))  # width:20, height:3

            # plt.bar((locationKeys), var022, align='edge', width=0.3)

            # Figures out the absolute path for you in case your working directory moves around.
            my_path = str(Path(__file__).parent)
                
            metricsFilePath = metricsFilePath.split('/')[2]

            metricsFilePath = metricsFilePath.replace(r'.', '')   
        
            metricsFilePath = metricsFilePath.replace(r'/', '')
            
            metricsFilePath = metricsFilePath.replace('json', '')

            plt.savefig(my_path + '\\..\\results\\' + '1 - ' + metricsFilePath + '.png')

            rootAFilePathIndex += 1

            print(probeIdWithSameCountryResponsePercentage)

            print('Probes with always same origin response: ' +
                str(probeIdWithAlwaysSameCountryResponsePercentage))

    # ROOT A 2022 END

    # ROOT A 2017 START

    filePath = '../probesData/20170824.json'

    metricsFilePaths = ['../metrics/Medição 2 A IPV4.json',
                        '../metrics/Medição 4 A IPV6.json']

    path = Path(__file__).parent / str(filePath)

    locationCountriesFilePath = './util/LocationCountries.json'

    locationCountriesPath = Path(__file__).parent / str(locationCountriesFilePath)

    rootAFilePathIndex = 1

    for metricsFilePath in metricsFilePaths:

        with path.open() as f:

            data = json.load(f)

            probeIdProbeOriginDict = probesDataParse.parseProbesData(data)

            probeIdWithSameCountryResponsePercentage = 0

            probeIdWithSameCountryResponsePercentage = 0

            probeIdWithSameCountryResponseCount = 0

            probeIdWithAlwaysSameCountryResponseCount = 0

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

            # REPLACE END

            percentageOfActiveProbes = 0

            print('Total probes: ' + str(len(probeIdProbeOriginDict)))

            print('Total active probes: ' + str(totalActiveProbesIPV4))

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

                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and alreadyCalculatedProbeId < 1):

                            probeIdWithSameCountryResponseCount += 1

                            alreadyCalculatedProbeId = 1

                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper()):

                            countAlwaysInSameCountryFromOrigin += 1

                        # ALWAYS FROM SAME ORIGIN ( 2 responses from same origin of the request )
                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and countAlwaysInSameCountryFromOrigin > 1):

                            probeIdWithAlwaysSameCountryResponseCount += 1

            probeIdWithSameCountryResponsePercentage = probeIdWithSameCountryResponseCount * \
                100 / totalActiveProbesIPV4 if probeIdWithSameCountryResponseCount > 0 else 0

            probeIdWithAlwaysSameCountryResponsePercentage = probeIdWithAlwaysSameCountryResponseCount * \
                100 / totalActiveProbesIPV4 if probeIdWithAlwaysSameCountryResponseCount > 0 else 0

            print(probeIdWithSameCountryResponseCount)

            percentageWithNoResponsesFromSameCountry = 100 - probeIdWithSameCountryResponsePercentage

            # print()
            
            var022 = [probeIdWithSameCountryResponsePercentage, percentageWithNoResponsesFromSameCountry]

            yearOfMeasurement = '2017'

            # if (rootKFilePathIndex % 2 == 0):

            #     yearOfMeasurement = '2022'

            if (rootAFilePathIndex == 2):

                yearOfMeasurement += ' IPV6'

            else:

                yearOfMeasurement += ' IPV4'

            df = pd.DataFrame({
                # '2017': var2017,
                yearOfMeasurement: var022
            }, index=['Probes que receberam resposta do mesmo país onde estão localizadas', 'Probes que não receberam nenhuma resposta do mesmo país onde estão localizadas'])

            ax = df.plot(subplots=True, kind='pie',
                        figsize=(28, 24), autopct='%1.1f%%')

            # plt.figure(figsize=(20, 3))  # width:20, height:3

            # plt.bar((locationKeys), var022, align='edge', width=0.3)

            # Figures out the absolute path for you in case your working directory moves around.
            my_path = str(Path(__file__).parent)
                
            metricsFilePath = metricsFilePath.split('/')[2]

            metricsFilePath = metricsFilePath.replace(r'.', '')   
        
            metricsFilePath = metricsFilePath.replace(r'/', '')
            
            metricsFilePath = metricsFilePath.replace('json', '')

            plt.savefig(my_path + '\\..\\results\\' + '1 - ' + metricsFilePath + '.png')

            rootAFilePathIndex += 1

            print(probeIdWithSameCountryResponsePercentage)

            print('Probes with always same origin response: ' +
                str(probeIdWithAlwaysSameCountryResponsePercentage))

    # ROOT A 2017 END


    # ROOT K 2022 START

    filePath = '../probesData/20220824.json'

    metricsFilePaths = ['../metrics/Medição 5 K IPV4.json',
                        '../metrics/Medição 7 K IPV6.json'
                        ]

    path = Path(__file__).parent / str(filePath)

    # CRUZAR DADOS DO ARQUIVO DE PROBES E DO ARQUIVO DE MÉTRICAS

    # 1 - K -> OK, A -> OK
    # PORCENTAGEM DE PROBES SE CONECTAM AO MESMO PAÍS DE ORIGEM

    # 2 -
    # PORCENTAGEM DE PROBES QUE SE CONECTAM EM PAÍSES DIFERENTES EM IPV4 E IPV6

    # 3 -
    # PORCENTAGEM DE PROBES QUE SE CONECTAM AO MESMO PAÍS DE ORIGEM EM UM PROTOCOLO E EM OUTRO NÃO

    # print(probeIdProbeOriginDict)

    # 1 - K - OK
    # PORCENTAGEM DE PROBES SE CONECTAM AO MESMO PAÍS DE ORIGEM
    
    rootKFilePathIndex = 1
    
    for metricsFilePath in metricsFilePaths:

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

            for probeKey in probeIdCountryResponseIPV4:

                alreadyCalculatedProbeId = 0

                probeCountryResponses = probeIdCountryResponseIPV4[probeKey]

                # ALWAYS FROM SAME ORIGIN COUNTER
                countAlwaysInSameCountryFromOrigin = 0

                count = 0

                for country in probeCountryResponses:

                    # JUST COUNT FIRST 2 RESPONSES
                    if (str(probeKey) in probeIdProbeOriginDict and count < 2):

                        count += 1

                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and alreadyCalculatedProbeId < 1):

                            probeIdWithSameCountryResponseCount += 1

                            alreadyCalculatedProbeId = 1

                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper()):

                            countAlwaysInSameCountryFromOrigin += 1

                        # ALWAYS FROM SAME ORIGIN ( 2 responses from same origin of the request )
                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and countAlwaysInSameCountryFromOrigin > 1):

                            probeIdWithAlwaysSameCountryResponseCount += 1

            probeIdWithSameCountryResponsePercentage = probeIdWithSameCountryResponseCount * \
                100 / totalActiveProbesIPV4 if probeIdWithSameCountryResponseCount > 0 else 0

            probeIdWithAlwaysSameCountryResponsePercentage = probeIdWithAlwaysSameCountryResponseCount * \
                100 / totalActiveProbesIPV4 if probeIdWithAlwaysSameCountryResponseCount > 0 else 0

            print(probeIdWithSameCountryResponseCount)

            percentageWithNoResponsesFromSameCountry = 100 - probeIdWithSameCountryResponsePercentage

            # print()
            
            var022 = [probeIdWithSameCountryResponsePercentage, percentageWithNoResponsesFromSameCountry]

            yearOfMeasurement = '2022'

            # if (rootKFilePathIndex % 2 == 0):

            #     yearOfMeasurement = '2022'

            if (rootKFilePathIndex == 2):

                yearOfMeasurement += ' IPV6'

            else:

                yearOfMeasurement += ' IPV4'

            df = pd.DataFrame({
                # '2017': var2017,
                yearOfMeasurement: var022
            }, index=['Probes que receberam resposta do mesmo país onde estão localizadas', 'Probes que não receberam nenhuma resposta do mesmo país onde estão localizadas'])

            ax = df.plot(subplots=True, kind='pie',
                        figsize=(28, 24), autopct='%1.1f%%')

            # plt.figure(figsize=(20, 3))  # width:20, height:3

            # plt.bar((locationKeys), var022, align='edge', width=0.3)

            # Figures out the absolute path for you in case your working directory moves around.
            my_path = str(Path(__file__).parent)
                
            metricsFilePath = metricsFilePath.split('/')[2]

            metricsFilePath = metricsFilePath.replace(r'.', '')   
        
            metricsFilePath = metricsFilePath.replace(r'/', '')
            
            metricsFilePath = metricsFilePath.replace('json', '')

            plt.savefig(my_path + '\\..\\results\\' + '1 - ' + metricsFilePath + '.png')

            rootKFilePathIndex += 1

            print(probeIdWithSameCountryResponsePercentage)

            print('Probes with always same origin response: ' +
                str(probeIdWithAlwaysSameCountryResponsePercentage))

    # ROOT K 2022 END
    
    
    # ROOT K 2017  START

    filePath = '../probesData/20170824.json'

    metricsFilePaths = ['../metrics/Medição 6 K IPV4.json',
                        '../metrics/Medição 8 K IPV6.json'
                        ]

    path = Path(__file__).parent / str(filePath)

    # ROOT K 
    
    rootKFilePathIndex = 1
    
    for metricsFilePath in metricsFilePaths:

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

            for probeKey in probeIdCountryResponseIPV4:

                alreadyCalculatedProbeId = 0

                probeCountryResponses = probeIdCountryResponseIPV4[probeKey]

                # ALWAYS FROM SAME ORIGIN COUNTER
                countAlwaysInSameCountryFromOrigin = 0

                count = 0

                for country in probeCountryResponses:

                    # JUST COUNT FIRST 2 RESPONSES
                    if (str(probeKey) in probeIdProbeOriginDict and count < 2):

                        count += 1

                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and alreadyCalculatedProbeId < 1):

                            probeIdWithSameCountryResponseCount += 1

                            alreadyCalculatedProbeId = 1

                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper()):

                            countAlwaysInSameCountryFromOrigin += 1

                        # ALWAYS FROM SAME ORIGIN ( 2 responses from same origin of the request )
                        if (probeIdProbeOriginDict[str(probeKey)] == str(country).upper() and countAlwaysInSameCountryFromOrigin > 1):

                            probeIdWithAlwaysSameCountryResponseCount += 1

            probeIdWithSameCountryResponsePercentage = probeIdWithSameCountryResponseCount * \
                100 / totalActiveProbesIPV4 if probeIdWithSameCountryResponseCount > 0 else 0

            probeIdWithAlwaysSameCountryResponsePercentage = probeIdWithAlwaysSameCountryResponseCount * \
                100 / totalActiveProbesIPV4 if probeIdWithAlwaysSameCountryResponseCount > 0 else 0

            print(probeIdWithSameCountryResponseCount)

            percentageWithNoResponsesFromSameCountry = 100 - probeIdWithSameCountryResponsePercentage

            # print()
            
            var022 = [probeIdWithSameCountryResponsePercentage, percentageWithNoResponsesFromSameCountry]

            yearOfMeasurement = '2017'

            # if (rootKFilePathIndex % 2 == 0):

            #     yearOfMeasurement = '2022'

            if (rootKFilePathIndex == 2):

                yearOfMeasurement += ' IPV6'

            else:

                yearOfMeasurement += ' IPV4'

            df = pd.DataFrame({
                # '2017': var2017,
                yearOfMeasurement: var022
            }, index=['Probes que receberam resposta do mesmo país onde estão localizadas', 'Probes que não receberam nenhuma resposta do mesmo país onde estão localizadas'])

            ax = df.plot(subplots=True, kind='pie',
                        figsize=(28, 24), autopct='%1.1f%%')

            # plt.figure(figsize=(20, 3))  # width:20, height:3

            # plt.bar((locationKeys), var022, align='edge', width=0.3)

            # Figures out the absolute path for you in case your working directory moves around.
            my_path = str(Path(__file__).parent)
                
            metricsFilePath = metricsFilePath.split('/')[2]

            metricsFilePath = metricsFilePath.replace(r'.', '')   
        
            metricsFilePath = metricsFilePath.replace(r'/', '')
            
            metricsFilePath = metricsFilePath.replace('json', '')

            plt.savefig(my_path + '\\..\\results\\' + '1 - ' + metricsFilePath + '.png')

            rootKFilePathIndex += 1

            print(probeIdWithSameCountryResponsePercentage)

            print('Probes with always same origin response: ' +
                str(probeIdWithAlwaysSameCountryResponsePercentage))

    # ROOT K 2017 END

    # 1 END
