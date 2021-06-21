import json

def Chemo(rbodysurf,  chemoType):
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
        
    print ("""         
                       NC""", chemoJson["NC"], """. deň
                                            """)
    
    Day1 = chemoJson["Day1"]["Instructions"]
    C1 = chemoJson["Chemo"]
    
    print("                                     D1")
    print (chemoJson["Day1"]["Premed"]["Note"])
    
    for x in range(len(chemoJson["Chemo"])):
        print (Day1[x]["Name"], C1[x]["Dosage"]*rbodysurf,"mg", Day1[x]["Inst"] )
        
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

def hematology(rbodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane v hematoonkologii"""
    hem=str(input("""Aku chemoterapiu chcete podat?  
a) ABVD
b) CHOP
c) miniCHOP
d) DHAP
e) bendamustin
f) GemOx
g) Rituximab\n"""))
    
    if hem=="a":
        Chemo(rbodysurf,"ABVD.json")
    elif hem=="b":
        Chemo(rbodysurf,"CHOP.json")
    elif hem=="c":
        Chemo(rbodysurf,"miniCHOP.json")
    elif hem=="d":
        ChemoDDP(rbodysurf,"DHAP.json")
    elif hem=="e":
        Chemo(rbodysurf,"bendamustin.json")
    elif hem=="f":
        Chemo(rbodysurf,"Gemox.json")
    elif hem=="g":
        Chemo(rbodysurf,"rituximab.json")
    else:
        print("""Musite zadat a-g!""")
        hematology(rbodysurf)        

def breast(rbodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane v liecbe karcinomu prsnika"""
    brs=str(input("""Aku chemoterapiu chcete podat?  
a) EC
b) AC
c) dd-AC + G-CSF
d) docetaxel + G-CSF
e) paclitaxel
f) kapecitabin
g) gemcitabin
h) ribociclib
i) palbociclib
j) vinorelbin p.o. weekly
k) eribulin
l) peg- doxorubicin
m) TD-M1\n"""))
    
    if brs=="a":
    	Chemo(rbodysurf,"EC.json")
    elif brs=="b":
        Chemo(rbodysurf, "AC.json")
    elif brs=="c":
        Chemo(rbodysurf,"dd-AC.json")
    elif brs=="d":
        Chemo(rbodysurf,"docetaxelbreast.json")
    elif brs=="e":
        Chemo(rbodysurf,"paclitaxelweekly.json")
    elif brs=="f":
        Chemo(rbodysurf,"capecitabine.json")
    elif brs=="g":
        Chemo(rbodysurf,"gemcitabine.json")
    elif brs=="h":
      	Chemo(rbodysurf,"ribociclib.json")
    elif brs=="i":
        Chemo(rbodysurf,"palbociclib.json")
    elif brs=="j":
        Chemo(rbodysurf,"vinorelbinweekly.json")
    elif brs=="k":
        Chemo(rbodysurf,"eribulin.json")
    elif brs=="l":
        Chemo(rbodysurf,"pegdoxo.json")
    elif brs=="m":
        Chemo(rbodysurf,"TDM1.json")
    else:   
        print("""Musite zadat a-m!""")
        breast(rbodysurf)

                
def diagnosis(rbodysurf):
    """Tato funkcia urobi prvu triaz podla diagnozy"""
    while True:
        try:
            x=int(input("""Aku diagnozu idete liecit?  
1.) hematologicke malignity
2.) karcinom prsnika
3.) karcinom pluc
4.) kolorektalny karcinom
5.) ine GIT malignity
6.) karcinom hlavy a krku
7.) sarkomy
8.) karcinom prostaty
9.) ine urogenitalne malignity
10.) gynekologicke malignity
11.) imunoterapia
"""))
            assert 0 < x < 13
  
        except ValueError:
            print("Musite zadat cele cislo" )
            diagnosis()
        
        except AssertionError:
            print("Povolene hodnotry su od 1 do 12!")
            diagnosis()
        else:
            break
        
    
    if x==1:
        hematology(rbodysurf)
    elif x==2:
        breast(rbodysurf)
    elif x==3:
        lung(rbodysurf)
    elif x==4:
        colorectal(rbodysurf)
    elif x==5:
        git(rbodysurf)
    elif x==6:
        headandneck(rbodysurf)
    elif x==7:
        sarcoma(rbodysurf)
    elif x==8:
        prostate(rbodysurf)
    elif x==9:
        urogenital(rbodysurf)
    elif x==10:
        female(rbodysurf)
    elif x==11:
        immunotherapy(rbodysurf)
    

def bsa(weight, height):
    bodysurf= (weight**0.425)*(height**0.725)*0.007184
    rbodysurf= round(bodysurf,2)
    print("""Telesný povrch je:""", rbodysurf,"""m2
                                          """)
    diagnosis(rbodysurf)
    
def inpt():
    
    while True:
        try:
            w=int(input("Zadajte hmotnosť (kg):   "))
            assert 0 < w < 250
            
        except ValueError:
            print("Musíte zadať celé číslo!" )
        except AssertionError:
            print("Povolené hodnoty sú od 1 do 250!")
        else:
            break
       
    while True:
        try:
            h=int(input("Zadajte výšku (cm):     "))
            assert 0 < h < 250
            
        except ValueError:
            print("Musíte zadať celé číslo!" )
        
        except AssertionError:
            print("Povolené hodnoty sú od 1 do 250!")
        else:
            break
            
           
    bsa(w, h)
    
print("""-------Vitajte v programe ChemoThon v1.0 !! -------------------
Program kedykoľvek ukončíte kombináciou CTRL-C """)
inpt()