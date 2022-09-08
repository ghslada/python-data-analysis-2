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
import answer1

answer1.resolveAnswer1()

# 2 START

# PORCENTAGEM DE PROBES QUE SE CONECTAM EM PAÍSES DIFERENTES EM IPV4 E IPV6


filePath = '../probesData/20220824.json'

metricsFilePaths = ['../metrics/Medição 5 K IPV4.json',
                    '../metrics/Medição 7 K IPV6.json'
                    ]

path = Path(__file__).parent / str(filePath)

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

# # for probeKey in probeIdCountryResponseIPV4 :

# #     alreadyCalculatedProbeId = 0

# #     probeCountryResponses = probeIdCountryResponseIPV4[probeKey]

# #     # ALWAYS FROM SAME ORIGIN COUNTER
# #     countAlwaysInSameCountryFromOrigin = 0

# #     count = 0

# #     for country in probeCountryResponses :
