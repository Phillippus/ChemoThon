import json

def flatdoser(rbodysurf,chemoType, chemoFlat):
    chemoFile = open(chemoType, "r")
    chemoJson = json.loads(chemoFile.read())
    chemoFile.close()
    
    chemoFile2 = open(chemoFlat, "r")
    chemoJson2 = json.loads(chemoFile2.read())
    chemoFile2.close()
    
    
    
    for i in chemoJson["Chemo"] :
        print(i["Name"], " ", 
        round(i["Dosage"],2),
        i["DosageMetric"],".........",
        round(i["Dosage"]*rbodysurf,2),
        "mg D",
        i["Day"])
    
    for i in chemoJson2["Chemo"] :
        print(i["Name"], " ",
        round(i["Dosage"],2),
        i["DosageMetric"],".........",
        round(i["Dosage"],2),
        "mg D",
        i["Day"])
        
    print ("""         
                       NC""", chemoJson["NC"], """. deň
                                            """)
    
    Day1 = chemoJson["Day1"]["Instructions"]
    DayF1= chemoJson2["Day1"]["Instructions"]
    C1 = chemoJson["Chemo"]
    CF = chemoJson2["Chemo"]
    
    print("                                     D1")
    print (chemoJson["Day1"]["Premed"]["Note"])
    
    for x in range(len(chemoJson["Chemo"])):
        print (Day1[x]["Name"], round(C1[x]["Dosage"]*rbodysurf,2),"mg", Day1[x]["Inst"] )
    for y in range(len(chemoJson2["Chemo"])):
        print (DayF1[y]["Name"], round(CF[y]["Dosage"]),"mg", DayF1[y]["Inst"] )
        

flatdoser(1.86,"docetaxelprostate.json", "flatprednison.json")