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

def parseRootKHostnameLocation( answers ) :

    answer = str(answers[0]['RDATA'][0])

    answerFromCountry = ''

    # print(answer)

    if ('-' in answer ) :

        if ( '.' in answer ) :
    
            answer = answer.split('.', 2)[1]
            
    answerFromCountry = answer
        
    if ( '-' in answer ) :

        answerFromCountry = answerFromCountry.split('-', 2)[1]

        answerFromCountry = answerFromCountry.split('.', 2)[0]
        
        answerFromCountry = re.sub(r'[0-9]', '', answerFromCountry)

        answerFromCountry = re.sub(r'-', '', answerFromCountry)
        
        # print(answerFromCountry)
        
    else :

        answerFromCountry = answer
        # print(answerFromCountry)
        # exit()
    
    return answerFromCountry



def parseRootKHostnameCountry( answers ) :

    answer = str(answers[0]['RDATA'][0])

    answerFromCountry = ''

    # print(answer)
    
    # # exit()
        
    if ('-' in answer ) :
        
        if ( '.' in answer ) :
    
            answer = answer.split('.', 2)[1]
                
    answerFromCountry = answer
    
    # print(answerFromCountry)
    
    if ( '-' in answer ) :
           
        answerFromCountry = answerFromCountry.split('-', 2)[0]

        # answerFromCountry = answerFromCountry.split('.', 2)[1]
        
        answerFromCountry = re.sub(r'[0-9]', '', answerFromCountry)

        answerFromCountry = re.sub(r'-', '', answerFromCountry)
        
        # print(answerFromCountry)
        
    else :

        answerFromCountry = answer
        # print(answerFromCountry)
      
    return answerFromCountry


def parseMetrics (filePath) :
    
    print(filePath)
        
    path = Path(__file__).parent / str(filePath)
    
    with path.open() as f:

        data = json.load(f)

        index = 0

        resultsByIpSrc = {}

        resultsWithoutAnswers = []
        
        answersCount = 0

        errorsCount = 0

        print('\nResults: \n')
        
        differentDestinations = []
        
        differentDestinationsCount = 0

        destination = ''

        answersFromProbeCount = []
        
        locationCountryDict = {}

        for medicao in data :
                    
            # Se não houver erro na requisição                    
                    
            if ( 'error' not in medicao ) :
                
                destination = medicao['dst_addr']
            
                # Considera apenas resultados com destino IPV4 válido
                
                if( len(destination) > 9 ):
            
                    resultado = medicao['result']  
                    
                    # Se a requisição tiver retornado uma resposta
                    
                    if ( resultado['ANCOUNT'] > 0 ) :
                        
                        # Se o array de respostas não existir
                        
                        if ( 'answers' not in  resultado  ) :
                        
                            resultsWithoutAnswers.append(medicao)  
                            
                            errorsCount+=1      
                            
                        else :

                            answers = resultado['answers']

                            # print(answers)                

                            # Se houver alguma resposta no array

                            if( len(answers) > 0 ) :

                                # Parse do nome do servidor, para buscar apenas a localidade
                                
                                answers = resultado['answers']

                                # print(answers)                

                                # Se houver alguma resposta no array

                                if( len(answers) > 0 ) :

                                    # Parse do nome do servidor, para buscar apenas a localidade

                                    answerFromCountry = ''

                                    if ( 'k.ripe.net' in str(answers[0]['RDATA'][0]) ) :
        
                                        answerFromCountry = rootKParse.parseRootKHostnameCountry(answers)
                                        answerFromLocation = rootKParse.parseRootKHostnameLocation(answers)

                                        # JSON CONTENDO LOCALIZACAO COMO CHAVE E PAIS COMO VALOR
                                        locationCountryDict[answerFromLocation] = answerFromCountry
                                        


                                    # Se a chave do IP de origem já existir nos resultados    
                                        
                                    if ( medicao['prb_id'] in resultsByIpSrc and answerFromCountry != '' ):
                                        
                                        if ( len(resultsByIpSrc[medicao['prb_id']] ) < 2 ) : 
                                            
                                            resultsByIpSrc[medicao['prb_id']].append( answerFromCountry )        
                                            
                                    else:

                                        if ( answerFromCountry != '' ) :
                                            
                                            # Inicializa a chave no dicionário com o endereço de origem da requisição 
                                            # atribuindo o valor de um array com o primeiro valor a primeira resposta contendo a localidade do servidor K
                                            
                                            resultsByIpSrc[medicao['prb_id']] = [ answerFromCountry ]        

                                    # Incrementa o número de respostas com sucesso
                                    answersCount+=1
                        
                    else :
                        
                        # Incrementa o número de respostas com erro
                        errorsCount+=1

            else: 
                
                errorsCount+=1

            index+=1

        # print('Answers count: '+str(answersCount))
        
        # print('Requests with error: '+str(errorsCount))
                
        # print('\nResults without answers: \n')

        # print(json.dumps(resultsWithoutAnswers, indent=4))

        saveLocationCountryJson.save(locationCountryDict)

        print('\nResults by IP source: \n'+json.dumps(resultsByIpSrc))
        
        return resultsByIpSrc
