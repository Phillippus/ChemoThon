import json

def flatdoser(rbodysurf,chemoType):
    """táto funkcia rozpisuje chemoterapie, ktoré majú v tele flat-dose chemo"""
   
    chemoFile = open(chemoType, "r")
    chemoJson = json.loads(chemoFile.read())
    chemoFile.close()
    
    for i in chemoJson["Chemo"] :
        print(i["Name"], " ", 
             i["Dosage"], 
             i["DosageMetric"], " .....",
             i["Dosage"]*rbodysurf,
             "mg D",
             i["Day"])
    
    for e in chemoJson["FlatChemo"] :
         print(e["Name"], " ", 
             e["Dosage"], 
             e["DosageMetric"], " .....",
             e["Dosage"],
             "mg D",
             e["Day"])
        
    print ("""         
                       NC""", chemoJson["NC"], """. deň
                                            """)
    
    Day1 = chemoJson["Day1"]["Instructions"]
    C1 = chemoJson["Chemo"]
    C2 = chemoJson["FlatChemo"]
    
    print("                                     D1")
    print (chemoJson["Day1"]["Premed"]["Note"])
    
    for x in range(len(chemoJson["Chemo"])):
        print (Day1[x]["Name"], C1[x]["Dosage"]*rbodysurf,"mg", Day1[x]["Inst"] )
    for y in range(len(chemoJson["FlatChemo"])):
        print (Day1[y]["Name"], C2[y]["Dosage"],"mg", Day1[y]["Inst"] )
    

flatdoser(2,"DHAP.json")
