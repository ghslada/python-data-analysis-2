import json

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

import saveLocationCountryJson
import probesDataParse

import rootAParse
import rootKParse

# 2 START

# PORCENTAGEM DE PROBES QUE SE CONECTAM EM PAÍSES DIFERENTES EM IPV4 E IPV6
# PORCENTAGEM DE PROBES QUE SE CONECTAM EM PELO MENOS 1 PAÍS DIFERENTE EM IPV4 E IPV6

def resolveAnswer2() :

    filePath = '../probesData/20220824.json'

    metricsFilePaths = ['../metrics/Medição 5 K IPV4.json',
                        '../metrics/Medição 7 K IPV6.json'
                        ]

    path = Path(__file__).parent / str(filePath)

    probeIdCountryResponseIPV4 = {}

    probeIdCountryResponseIPV6 = {}

    totalActiveProbesIPV4 = 0

    totalActiveProbesIPV6 = 0

    rootKFilePathIndex = 1

    for metricsFilePath in metricsFilePaths :

        with path.open() as f:

            data = json.load(f)

            probeIdProbeOriginDict = probesDataParse.parseProbesData(data)

            # probeIdWithSameCountryResponsePercentage = 0

            # probeIdWithSameCountryResponsePercentage = 0

            # probeIdWithSameCountryResponseCount = 0

            # probeIdWithAlwaysSameCountryResponseCount = 0

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
    
    probeIdsWithSameCountryResponseInBothProtocols = 0
     
    alreadyCalculatedProbes = []    
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = 0
    # totalActiveProbesIPV6
    # totalActiveProbesIPV4
    
    # PORCENTAGEM DE PROBES EM IPV4 COM RESPOSTA DE MESMO PAÍS EM IPV6
    for probeId in probeIdCountryResponseIPV4 :
        
        # VERIFICA SE A MESMA PROBE TAMBEM ESTÁ NO IPV6
        if probeId in probeIdCountryResponseIPV6 :
            
            for country in probeIdCountryResponseIPV6[probeId] :
            
                # VERIFICA SE UM DOS PAÍSES DAS 2 REQUISIÇÕES DO IPV6 ESTÁ NA LISTA DE PAÍSES DA REQUISIÇÃO DA MESMA PROBE EM IPV4
                if country in probeIdCountryResponseIPV4[probeId] not in alreadyCalculatedProbes :
                    
                    alreadyCalculatedProbes.append(probeId)
                    probeIdsWithSameCountryResponseInBothProtocols+=1

    print( str(probeIdsWithSameCountryResponseInBothProtocols) + ' of '+ str(totalActiveProbesIPV4) + ' probes received at least one response from same country in IPV4' )


    probeIdsWithSameCountryResponseInBothProtocolsPercentage = probeIdsWithSameCountryResponseInBothProtocols * 100 / totalActiveProbesIPV4
    
    print('Percentage of probes with same response in IPV4: '+ str(probeIdsWithSameCountryResponseInBothProtocolsPercentage))
    
    percentageOfProbesWithResponsesAlwaysFromDifferentCountries = 100 - probeIdsWithSameCountryResponseInBothProtocolsPercentage

    var022 = [probeIdsWithSameCountryResponseInBothProtocolsPercentage, percentageOfProbesWithResponsesAlwaysFromDifferentCountries]

    yearOfMeasurement = '2022'
    
    if (rootKFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV4 que receberam pelo menos uma resposta do mesmo país nos protocolos IPV4 e IPV6', 'Probes do protocolo IPV4 que não receberam nenhuma resposta do mesmo país nos protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(28, 24), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
   
    metricsFilePath = '../metrics/Medição 5 A IPV4.json'
        
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '2 - ' + metricsFilePath + ' 2022.png')

    rootKFilePathIndex += 1

    ##################################
    # IPV4 END
    
    ###################################
    # IPV6 START

    probeIdsWithSameCountryResponseInBothProtocols = 0
     
    alreadyCalculatedProbes = []    
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = 0
           
    # PORCENTAGEM DE PROBES EM IPV6 COM RESPOSTA DE MESMO PAÍS EM IPV4
    for probeId in probeIdCountryResponseIPV6 :
        
        # VERIFICA SE A MESMA PROBE TAMBEM ESTÁ NO IPV6
        if probeId in probeIdCountryResponseIPV4 :
            
            for country in probeIdCountryResponseIPV4[probeId] :
            
                # VERIFICA SE UM DOS PAÍSES DAS 2 REQUISIÇÕES DO IPV6 ESTÁ NA LISTA DE PAÍSES DA REQUISIÇÃO DA MESMA PROBE EM IPV4
                if country in probeIdCountryResponseIPV6[probeId] and probeId not in alreadyCalculatedProbes :
                    
                    alreadyCalculatedProbes.append(probeId)
                    probeIdsWithSameCountryResponseInBothProtocols+=1
            
    print( str(probeIdsWithSameCountryResponseInBothProtocols) + ' of '+ str(totalActiveProbesIPV6) + ' probes received at least one response from same country in IPV6' )
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = probeIdsWithSameCountryResponseInBothProtocols * 100 / totalActiveProbesIPV6
    
    print('Percentage of probes with same response in IPV6: '+ str(probeIdsWithSameCountryResponseInBothProtocolsPercentage))
        
    percentageOfProbesWithResponsesAlwaysFromDifferentCountries = 100 - probeIdsWithSameCountryResponseInBothProtocolsPercentage

    var022 = [probeIdsWithSameCountryResponseInBothProtocolsPercentage, percentageOfProbesWithResponsesAlwaysFromDifferentCountries]

    yearOfMeasurement = '2022'
    
    if (rootKFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV6 que receberam pelo menos uma resposta do mesmo país nos protocolos IPV4 e IPV6', 'Probes do protocolo IPV6 que não receberam nenhuma resposta do mesmo país nos protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(28, 24), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
   
    metricsFilePath = '../metrics/Medição 7 A IPV6.json'
        
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '2 - ' + metricsFilePath + ' 2022.png')

    rootKFilePathIndex += 1

    
    ###################################################################
    # ROOT K 2022 END
    
    ####################################################################
    # ROOT K 2017 START
    
    
    filePath = '../probesData/20170824.json'

    metricsFilePaths = ['../metrics/Medição 6 K IPV4.json',
                        '../metrics/Medição 8 K IPV6.json'
                        ]

    path = Path(__file__).parent / str(filePath)

    probeIdCountryResponseIPV4 = {}

    probeIdCountryResponseIPV6 = {}

    totalActiveProbesIPV4 = 0

    totalActiveProbesIPV6 = 0

    rootKFilePathIndex = 1

    for metricsFilePath in metricsFilePaths :

        with path.open() as f:

            data = json.load(f)

            probeIdProbeOriginDict = probesDataParse.parseProbesData(data)

            # probeIdWithSameCountryResponsePercentage = 0

            # probeIdWithSameCountryResponsePercentage = 0

            # probeIdWithSameCountryResponseCount = 0

            # probeIdWithAlwaysSameCountryResponseCount = 0

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
    
    probeIdsWithSameCountryResponseInBothProtocols = 0
     
    alreadyCalculatedProbes = []    
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = 0
    
    # totalActiveProbesIPV6
    # totalActiveProbesIPV4
    
    # PORCENTAGEM DE PROBES EM IPV4 COM RESPOSTA DE MESMO PAÍS EM IPV6
    for probeId in probeIdCountryResponseIPV4 :
        
        # VERIFICA SE A MESMA PROBE TAMBEM ESTÁ NO IPV6
        if probeId in probeIdCountryResponseIPV6 :
            
            for country in probeIdCountryResponseIPV6[probeId] :
            
                # VERIFICA SE UM DOS PAÍSES DAS 2 REQUISIÇÕES DO IPV6 ESTÁ NA LISTA DE PAÍSES DA REQUISIÇÃO DA MESMA PROBE EM IPV4
                if country in probeIdCountryResponseIPV4[probeId] not in alreadyCalculatedProbes :
                    
                    alreadyCalculatedProbes.append(probeId)
                    probeIdsWithSameCountryResponseInBothProtocols+=1

    print( str(probeIdsWithSameCountryResponseInBothProtocols) + ' of '+ str(totalActiveProbesIPV4) + ' probes received at least one response from same country in IPV4' )

    probeIdsWithSameCountryResponseInBothProtocolsPercentage = probeIdsWithSameCountryResponseInBothProtocols * 100 / totalActiveProbesIPV4
    
    print('Percentage of probes with same response in IPV4: '+ str(probeIdsWithSameCountryResponseInBothProtocolsPercentage))
    
    percentageOfProbesWithResponsesAlwaysFromDifferentCountries = 100 - probeIdsWithSameCountryResponseInBothProtocolsPercentage

    var022 = [probeIdsWithSameCountryResponseInBothProtocolsPercentage, percentageOfProbesWithResponsesAlwaysFromDifferentCountries]

    yearOfMeasurement = '2017'
    
    if (rootKFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV4 que receberam pelo menos uma resposta do mesmo país nos protocolos IPV4 e IPV6', 'Probes do protocolo IPV4 que não receberam nenhuma resposta do mesmo país nos protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(28, 24), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
    metricsFilePath = '../metrics/Medição 6 K IPV4.json'
        
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '2 - ' + metricsFilePath + ' 2017.png')

    rootKFilePathIndex += 1
    
    ############################
    # IPV6 START
    
    probeIdsWithSameCountryResponseInBothProtocols = 0
     
    alreadyCalculatedProbes = []    
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = 0
           
    # PORCENTAGEM DE PROBES EM IPV6 COM RESPOSTA DE MESMO PAÍS EM IPV4
    for probeId in probeIdCountryResponseIPV6 :
        
        # VERIFICA SE A MESMA PROBE TAMBEM ESTÁ NO IPV6
        if probeId in probeIdCountryResponseIPV4 :
            
            for country in probeIdCountryResponseIPV4[probeId] :
            
                # VERIFICA SE UM DOS PAÍSES DAS 2 REQUISIÇÕES DO IPV6 ESTÁ NA LISTA DE PAÍSES DA REQUISIÇÃO DA MESMA PROBE EM IPV4
                if country in probeIdCountryResponseIPV6[probeId] and probeId not in alreadyCalculatedProbes :
                    
                    alreadyCalculatedProbes.append(probeId)
                    probeIdsWithSameCountryResponseInBothProtocols+=1
            
    print( str(probeIdsWithSameCountryResponseInBothProtocols) + ' of '+ str(totalActiveProbesIPV6) + ' probes received at least one response from same country in IPV6' )
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = probeIdsWithSameCountryResponseInBothProtocols * 100 / totalActiveProbesIPV6
    
    print('Percentage of probes with same response in IPV6: '+ str(probeIdsWithSameCountryResponseInBothProtocolsPercentage))
    
    percentageOfProbesWithResponsesAlwaysFromDifferentCountries = 100 - probeIdsWithSameCountryResponseInBothProtocolsPercentage

    var022 = [probeIdsWithSameCountryResponseInBothProtocolsPercentage, percentageOfProbesWithResponsesAlwaysFromDifferentCountries]

    yearOfMeasurement = '2017'
    
    if (rootKFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV6 que receberam pelo menos uma resposta do mesmo país nos protocolos IPV4 e IPV6', 'Probes do protocolo IPV6 que não receberam nenhuma resposta do mesmo país nos protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(28, 24), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
   
    metricsFilePath = '../metrics/Medição 8 K IPV6.json'
        
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '2 - ' + metricsFilePath + ' 2017.png')

    rootKFilePathIndex += 1
 
    
    # ROOT K 2017 END
    ###############################################
    
    ###############################################
    # ROOT A 2022 START
    
    filePath = '../probesData/20220824.json'

    metricsFilePaths = ['../metrics/Medição 1 A IPV4.json',
                        '../metrics/Medição 3 A IPV6.json'
                        ]

    path = Path(__file__).parent / str(filePath)

    probeIdCountryResponseIPV4 = {}

    probeIdCountryResponseIPV6 = {}

    totalActiveProbesIPV4 = 0

    totalActiveProbesIPV6 = 0
    
    rootAFilePathIndex = 1
    
    for metricsFilePath in metricsFilePaths :

        with path.open() as f:

            data = json.load(f)

            probeIdProbeOriginDict = probesDataParse.parseProbesData(data)

            # probeIdWithSameCountryResponsePercentage = 0

            # probeIdWithSameCountryResponsePercentage = 0

            # probeIdWithSameCountryResponseCount = 0

            # probeIdWithAlwaysSameCountryResponseCount = 0

            if ( str(metricsFilePath).__contains__('IPV4') ) :

                probeIdCountryResponseIPV4 = rootAParse.parseMetrics(metricsFilePath)

                totalActiveProbesIPV4 = len(probeIdCountryResponseIPV4)

                percentageOfActiveProbes = 0

                print('Total probes: ' + str(len(probeIdProbeOriginDict)))

                print('Total active probes: ' + str(totalActiveProbesIPV4))

            else :

                probeIdCountryResponseIPV6 = rootAParse.parseMetrics(metricsFilePath)

                totalActiveProbesIPV6 = len(probeIdCountryResponseIPV6)

                percentageOfActiveProbes = 0

                print('Total probes: ' + str(len(probeIdProbeOriginDict)))

                print('Total active probes: ' + str(totalActiveProbesIPV6))

    saveLocationCountryJson.compareLocationsFromRootAWithLocationsFromRootK()
    
    probeIdsWithSameCountryResponseInBothProtocols = 0
     
    alreadyCalculatedProbes = []    
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = 0
    # totalActiveProbesIPV6
    # totalActiveProbesIPV4
    
    # PORCENTAGEM DE PROBES EM IPV4 COM RESPOSTA DE MESMO PAÍS EM IPV6
    for probeId in probeIdCountryResponseIPV4 :
        
        # VERIFICA SE A MESMA PROBE TAMBEM ESTÁ NO IPV6
        if probeId in probeIdCountryResponseIPV6 :
            
            for country in probeIdCountryResponseIPV6[probeId] :
            
                # VERIFICA SE UM DOS PAÍSES DAS 2 REQUISIÇÕES DO IPV6 ESTÁ NA LISTA DE PAÍSES DA REQUISIÇÃO DA MESMA PROBE EM IPV4
                if country in probeIdCountryResponseIPV4[probeId] not in alreadyCalculatedProbes :
                    
                    alreadyCalculatedProbes.append(probeId)
                    probeIdsWithSameCountryResponseInBothProtocols+=1

    print( str(probeIdsWithSameCountryResponseInBothProtocols) + ' of '+ str(totalActiveProbesIPV4) + ' probes received at least one response from same country in IPV4' )

    probeIdsWithSameCountryResponseInBothProtocolsPercentage = probeIdsWithSameCountryResponseInBothProtocols * 100 / totalActiveProbesIPV4
    
    print('Percentage of probes with same response in IPV4: '+ str(probeIdsWithSameCountryResponseInBothProtocolsPercentage))
        
    percentageOfProbesWithResponsesAlwaysFromDifferentCountries = 100 - probeIdsWithSameCountryResponseInBothProtocolsPercentage

    var022 = [probeIdsWithSameCountryResponseInBothProtocolsPercentage, percentageOfProbesWithResponsesAlwaysFromDifferentCountries]

    yearOfMeasurement = '2022'
    
    if (rootAFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV4 que receberam pelo menos uma resposta do mesmo país nos protocolos IPV4 e IPV6', 'Probes do protocolo IPV4 que não receberam nenhuma resposta do mesmo país nos protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(35, 26), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
    metricsFilePath = '../metrics/Medição 1 A IPV4.json'
   
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '2 - ' + metricsFilePath + ' 2022.png')

    rootAFilePathIndex += 1 
    
    ########################################################
    # IPV6 START

    probeIdsWithSameCountryResponseInBothProtocols = 0
     
    alreadyCalculatedProbes = []    
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = 0
           
    # PORCENTAGEM DE PROBES EM IPV6 COM RESPOSTA DE MESMO PAÍS EM IPV4
    for probeId in probeIdCountryResponseIPV6 :
        
        # VERIFICA SE A MESMA PROBE TAMBEM ESTÁ NO IPV6
        if probeId in probeIdCountryResponseIPV4 :
            
            for country in probeIdCountryResponseIPV4[probeId] :
            
                # VERIFICA SE UM DOS PAÍSES DAS 2 REQUISIÇÕES DO IPV6 ESTÁ NA LISTA DE PAÍSES DA REQUISIÇÃO DA MESMA PROBE EM IPV4
                if country in probeIdCountryResponseIPV6[probeId] and probeId not in alreadyCalculatedProbes :
                    
                    alreadyCalculatedProbes.append(probeId)
                    probeIdsWithSameCountryResponseInBothProtocols+=1
            
    print( str(probeIdsWithSameCountryResponseInBothProtocols) + ' of '+ str(totalActiveProbesIPV6) + ' probes received at least one response from same country in IPV6' )
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = probeIdsWithSameCountryResponseInBothProtocols * 100 / totalActiveProbesIPV6
    
    print('Percentage of probes with same response in IPV6: '+ str(probeIdsWithSameCountryResponseInBothProtocolsPercentage))
    
    percentageOfProbesWithResponsesAlwaysFromDifferentCountries = 100 - probeIdsWithSameCountryResponseInBothProtocolsPercentage

    var022 = [probeIdsWithSameCountryResponseInBothProtocolsPercentage, percentageOfProbesWithResponsesAlwaysFromDifferentCountries]

    yearOfMeasurement = '2022'
    
    if (rootAFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV6 que receberam pelo menos uma resposta do mesmo país nos protocolos IPV4 e IPV6', 'Probes do protocolo IPV6 que não receberam nenhuma resposta do mesmo país nos protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(32, 24), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
   
    metricsFilePath = '../metrics/Medição 3 A IPV6.json'
        
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '2 - ' + metricsFilePath + ' 2022.png')

    rootAFilePathIndex += 1

    # ROOT A 2022 END
    
    ####################################################################
    # ROOT A 2017 START
    
    filePath = '../probesData/20170824.json'

    metricsFilePaths = ['../metrics/Medição 2 A IPV4.json',
                        '../metrics/Medição 4 A IPV6.json'
                        ]

    path = Path(__file__).parent / str(filePath)

    probeIdCountryResponseIPV4 = {}

    probeIdCountryResponseIPV6 = {}

    totalActiveProbesIPV4 = 0

    totalActiveProbesIPV6 = 0

    rootAFilePathIndex = 1
    
    for metricsFilePath in metricsFilePaths :

        with path.open() as f:

            data = json.load(f)

            probeIdProbeOriginDict = probesDataParse.parseProbesData(data)

            # probeIdWithSameCountryResponsePercentage = 0

            # probeIdWithSameCountryResponsePercentage = 0

            # probeIdWithSameCountryResponseCount = 0

            # probeIdWithAlwaysSameCountryResponseCount = 0

            if ( str(metricsFilePath).__contains__('IPV4') ) :

                probeIdCountryResponseIPV4 = rootAParse.parseMetrics(metricsFilePath)

                totalActiveProbesIPV4 = len(probeIdCountryResponseIPV4)

                percentageOfActiveProbes = 0

                print('Total probes: ' + str(len(probeIdProbeOriginDict)))

                print('Total active probes: ' + str(totalActiveProbesIPV4))

            else :

                probeIdCountryResponseIPV6 = rootAParse.parseMetrics(metricsFilePath)

                totalActiveProbesIPV6 = len(probeIdCountryResponseIPV6)

                percentageOfActiveProbes = 0

                print('Total probes: ' + str(len(probeIdProbeOriginDict)))

                print('Total active probes: ' + str(totalActiveProbesIPV6))
                    
    saveLocationCountryJson.compareLocationsFromRootAWithLocationsFromRootK()
    
    probeIdsWithSameCountryResponseInBothProtocols = 0
     
    alreadyCalculatedProbes = []    
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = 0
    
    # totalActiveProbesIPV6
    # totalActiveProbesIPV4
    # NOVA ITERAÇÃO NOS FILEPATHS PARA SALVAR OS GRÁFICOS
    
    # PORCENTAGEM DE PROBES EM IPV4 COM RESPOSTA DE MESMO PAÍS EM IPV6
    for probeId in probeIdCountryResponseIPV4 :
        
        # VERIFICA SE A MESMA PROBE TAMBEM ESTÁ NO IPV6
        if probeId in probeIdCountryResponseIPV6 :
            
            for country in probeIdCountryResponseIPV6[probeId] :
            
                # VERIFICA SE UM DOS PAÍSES DAS 2 REQUISIÇÕES DO IPV6 ESTÁ NA LISTA DE PAÍSES DA REQUISIÇÃO DA MESMA PROBE EM IPV4
                if country in probeIdCountryResponseIPV4[probeId] not in alreadyCalculatedProbes :
                    
                    alreadyCalculatedProbes.append(probeId)
                    probeIdsWithSameCountryResponseInBothProtocols+=1

    print( str(probeIdsWithSameCountryResponseInBothProtocols) + ' of '+ str(totalActiveProbesIPV4) + ' probes received at least one response from same country in IPV4' )

    probeIdsWithSameCountryResponseInBothProtocolsPercentage = probeIdsWithSameCountryResponseInBothProtocols * 100 / totalActiveProbesIPV4

    percentageWithSameCountryMessage = 'Porcentagem de probes do protocolo IPV4 com respostas do mesmo país nos protocolos IPV4 e IPV6: '
    
    print(percentageWithSameCountryMessage + str(probeIdsWithSameCountryResponseInBothProtocolsPercentage))
    
    percentageOfProbesWithResponsesAlwaysFromDifferentCountries = 100 - probeIdsWithSameCountryResponseInBothProtocolsPercentage

    var022 = [probeIdsWithSameCountryResponseInBothProtocolsPercentage, percentageOfProbesWithResponsesAlwaysFromDifferentCountries]

    yearOfMeasurement = '2017'
    
    if (rootAFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV4 que receberam pelo menos uma resposta do mesmo país nos protocolos IPV4 e IPV6', 'Probes do protocolo IPV4 que não receberam nenhuma resposta do mesmo país nos protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(28, 24), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
   
    metricsFilePath = '../metrics/Medição 2 A IPV4.json'
    
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '2 - ' + metricsFilePath + ' 2017.png')

    rootAFilePathIndex += 1

    #######################################################
    # IPV6
    
    probeIdsWithSameCountryResponseInBothProtocols = 0
     
    alreadyCalculatedProbes = []    
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = 0
           
    # PORCENTAGEM DE PROBES EM IPV6 COM RESPOSTA DE MESMO PAÍS EM IPV4
    for probeId in probeIdCountryResponseIPV6 :
        
        # VERIFICA SE A MESMA PROBE TAMBEM ESTÁ NO IPV6
        if probeId in probeIdCountryResponseIPV4 :
            
            for country in probeIdCountryResponseIPV4[probeId] :
            
                # VERIFICA SE UM DOS PAÍSES DAS 2 REQUISIÇÕES DO IPV6 ESTÁ NA LISTA DE PAÍSES DA REQUISIÇÃO DA MESMA PROBE EM IPV4
                if country in probeIdCountryResponseIPV6[probeId] and probeId not in alreadyCalculatedProbes :
                    
                    alreadyCalculatedProbes.append(probeId)
                    probeIdsWithSameCountryResponseInBothProtocols+=1
            
    print( str(probeIdsWithSameCountryResponseInBothProtocols) + ' of '+ str(totalActiveProbesIPV6) + ' probes received at least one response from same country in IPV6' )
    
    probeIdsWithSameCountryResponseInBothProtocolsPercentage = probeIdsWithSameCountryResponseInBothProtocols * 100 / totalActiveProbesIPV6
   
    percentageWithSameCountryMessage = 'Porcentagem de probes do protocolo IPV6 com respostas do mesmo país nos protocolos IPV4 e IPV6: '
    
    print(percentageWithSameCountryMessage + str(probeIdsWithSameCountryResponseInBothProtocolsPercentage))
    
    percentageOfProbesWithResponsesAlwaysFromDifferentCountries = 100 - probeIdsWithSameCountryResponseInBothProtocolsPercentage

    var022 = [probeIdsWithSameCountryResponseInBothProtocolsPercentage, percentageOfProbesWithResponsesAlwaysFromDifferentCountries]

    yearOfMeasurement = '2017'
    
    
    if (rootAFilePathIndex >= 2):

        yearOfMeasurement += ' IPV6'

    else:

        yearOfMeasurement += ' IPV4'

    df = pd.DataFrame({
        # '2017': var2017,
        yearOfMeasurement: var022
        
    }, index=['Probes do protocolo IPV6 que receberam pelo menos uma resposta do mesmo país nos protocolos IPV4 e IPV6', 'Probes do protocolo IPV6 que não receberam nenhuma resposta do mesmo país nos protocolos IPV4 e IPV6'])

    ax = df.plot(subplots=True, kind='pie',
                figsize=(28, 24), autopct='%1.1f%%')

    # plt.figure(figsize=(20, 3))  # width:20, height:3

    # plt.bar((locationKeys), var022, align='edge', width=0.3)

    # Figures out the absolute path for you in case your working directory moves around.
    my_path = str(Path(__file__).parent)
       
    metricsFilePath = '../metrics/Medição 4 A IPV6.json'
           
    metricsFilePath = metricsFilePath.split('/')[2]

    metricsFilePath = metricsFilePath.replace(r'.', '')   

    metricsFilePath = metricsFilePath.replace(r'/', '')
    
    metricsFilePath = metricsFilePath.replace('json', '')

    plt.savefig(my_path + '\\..\\results\\' + '2 - ' + metricsFilePath + ' 2017.png')

    rootAFilePathIndex += 1
 