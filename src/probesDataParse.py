def parseProbesData (data) :
    
    probeIdProbeOriginDict = {}
    
    for object in data['objects'] :
        
        # "status_name": "Connected"
        
        # if object['status_name'] == 'Connected':
        
        probeIdProbeOriginDict[str(object['id'])] = object['country_code']
        # print(probeIdProbeOriginDict) 
    
    # print(probeIdProbeOriginDict)                
    
    return probeIdProbeOriginDict