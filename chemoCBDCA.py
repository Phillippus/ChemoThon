import json

def ChemoCBDCA(rbodysurf,chemoType):
    #Táto funkcia slúži pre rozpis chemoterapie obsahujúcu karboplatinu
    chemoFile = open(chemoType, "r")
    chemoJson = json.loads(chemoFile.read())
    chemoFile.close()
    
    while True:
        try:
            CrCl=int(input("Zadajte hodnotu clearance v ml/min     "))
            assert 0 < CrCl < 250
            
        except ValueError:
            print("Musíte zadať celé číslo!" )
        except AssertionError:
            print("Povolené hodnoty sú od 1 do 250!")
        else:
            break
        
    while True:
        try:
            AUC=int(input("Zadajte hodnotu AUC 2-6    "))
            assert 1 < AUC < 7
            
        except ValueError:
            print("Musíte zadať celé číslo!" )
        except AssertionError:
            print("Povolené hodnoty sú od 2 do 6!")
        else:
            break    
    
    print("CBDCA AUC",AUC,"............",(CrCl+25)*AUC,"mg  D1")        
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
    
    Day1 = chemoJson["Day1"]["Instructions"]
    C1 = chemoJson["Chemo"]
    
    print("""                                   
                                        D1
                                        """)
    print (chemoJson["Day1"]["Premed"]["Note"])
    print("CBDCA",(CrCl+25)*AUC,"mg v 500ml FR iv" )
    for x in range(len(chemoJson["Chemo"])):
        print (Day1[x]["Name"], C1[x]["Dosage"]*rbodysurf,"mg", Day1[x]["Inst"] )
        
rbodysurf=2
chemoType="gemcitabinDDP.json"
ChemoCBDCA(rbodysurf,chemoType)
