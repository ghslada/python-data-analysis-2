from ast import For
import pandas as pd
import matplotlib.pyplot as plt
import json
import rootAParse
import saveLocationCountryJson
from pathlib import Path
import re

def parseRootAHostname( answers ) :

    answer = str(answers[0]['RDATA'][0])

    answerFromCountry = ''

    if ( '-' in answer ) :

        answerFromCountry = answer.split('-', 2)[1]
            
        print(answerFromCountry)

        answerFromCountry = re.sub(r'[0-9]', '', answerFromCountry)

        answerFromCountry = re.sub(r'-', '', answerFromCountry)
        
        if ( len(answerFromCountry) <= 5 ) :
        
            if len(answerFromCountry) == 5 :
                
                answerFromCountry = answerFromCountry[2:]
        
        else :
            
            answerFromCountry = ''


    else :

        answerFromCountry = ''
            
            
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
        
        locationsFromRootA = {}

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

                            print(answers)                

                            # Se houver alguma resposta no array

                            if( len(answers) > 0 ) :

                                # Parse do nome do servidor, para buscar apenas a localidade

                                answerFromCountry = rootAParse.parseRootAHostname(answers)

                                # exit()
                                
                                # Se a chave do IP de origem já existir nos resultados    
                                    
                                if ( medicao['prb_id'] in resultsByIpSrc and len(answerFromCountry) > 1 ):
                                    
                                    resultsByIpSrc[medicao['prb_id']].append( answerFromCountry )  
                                    locationsFromRootA[answerFromCountry] = 1      

                                else:

                                    if len(answerFromCountry) > 1 :
    
                                        resultsByIpSrc[medicao['prb_id']] = [answerFromCountry]    
                                        locationsFromRootA[answerFromCountry] = 1    

                                # Incrementa o número de respostas com sucesso
                                answersCount+=1
                    
                    else :
                        
                        # Incrementa o número de respostas com erro
                        errorsCount+=1

            else: 
                
                errorsCount+=1

            index+=1

        print('Answers count: '+str(answersCount))
        
        print('Requests with error: '+str(errorsCount))
                
        print('\nResults without answers: \n')
        
        saveLocationCountryJson.saveLocationsFromRootA(locationsFromRootA)

        print(json.dumps(resultsWithoutAnswers, indent=4))

        print('\nResults by IP source: \n'+json.dumps(resultsByIpSrc))
        
        return resultsByIpSrc
