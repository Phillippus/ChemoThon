import json

def ChemoDDP(rbodysurf,  chemoType):
    #Táto funkcia slúži pre chemoterapie s DDP
    chemoFile = open(chemoType, "r")
    chemoJson = json.loads(chemoFile.read())
    chemoFile.close()
    
    print("DDP 80mg/m2................",80*rbodysurf,"mg  D1")
    for i in chemoJson["Chemo"] :
        print(i["Name"], " ", 
          i["Dosage"], 
          i["DosageMetric"], " .....",
          i["Dosage"]*rbodysurf,
          "mg D",
          i["Day"])
        
    print ("""
                   NC""", chemoJson["NC"], """. deň
           """)
    
    print("""                                  
                                          D1
                                          """)
    print ("1. ",chemoJson["Day1"]["Premed"]["Note"])

    a=80*rbodysurf
    b=a//50
    c=a%50
    rng=int(b)
    
    for ordo in range(2,rng+2):
        print(ordo, """. Cisplatina 50mg v 500ml RR iv""")
        ordo+=1
    print(ordo,""". Cisplatina""",int(c),"""mg v 500ml RR iv""")
    print(ordo+1,""". Manitol 10% 250ml iv""")
    
    Day1 = chemoJson["Day1"]["Instructions"]
    C1 = chemoJson["Chemo"]
      
    for x in range(len(chemoJson["Chemo"])):
        print (ordo+2,".",Day1[x]["Name"], C1[x]["Dosage"]*rbodysurf,"mg", Day1[x]["Inst"] )
        
    

rbodysurf=2
chemoType="gemcitabinDDP.json"
ChemoDDP(rbodysurf,chemoType)    