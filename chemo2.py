def Capox():
    print("""
Oxaliplatina 130mg/m2 .......""",130*rbodysurf,""" mg D1
kapecitabín 1000mg/m2 BID....""",2000*rbodysurf,""" mg D1-D14

                                NC 21 deň
                                
            
1. Granegis 2tbl/ Onsetrogen 8mg v 250ml FR iv
2. Oxaliplatina """, 130*rbodysurf,""" mg v 500ml 5%GLC iv
3. Kapecitabín """, 2000*rbodysurf, """mg p.o. rozdeliť na 2 dávky""")
    
def CapIri():
    print("""
Irinotekan 175mg/m2 .......""",175*rbodysurf,""" mg D1
kapecitabín 1000mg/m2 BID....""",2000*rbodysurf,""" mg D2-D8

                                NC 14 deň
                                
            
1. Granegis 2tbl/ Onsetrogen 8mg v 250ml FR iv
2. Irinotekan """, 175*rbodysurf,""" mg v 500ml FR iv
3. Kapecitabín """, 2000*rbodysurf, """mg p.o. rozdeliť na 2 dávky""")

def DDPGem():
    a=80*rbodysurf
    b=a//50
    c=a%50
    def subDDPGem():
        rng=int(b)
        for ordo in range(2,rng+2):
            print(ordo, """. Cisplatina 50mg v 500ml RR iv""")
            ordo+=1
        print(ordo,""". Cisplatina""",int(c),"""mg v 500ml RR iv""")
        print(ordo+1,""". Manitol 10% 250ml iv""")
        print(ordo+2,""". Gemcitabín""", int(1000*rbodysurf),"""mg v 500ml FR iv""")
    

    print("""
cisplatina 80mg/m2 .......""",int(80*rbodysurf),""" mg D1
gemcitabín 1000mg/m2 ....""",int(1000*rbodysurf),""" mg D1, D8 

                                NC 21 deň
                                
            
1. Granegis 2tbl, Dexametazon 8mg iv, Nolpaza 40mg p.o.""")
    subDDPGem()



def chemorozc():
    q=str(input("""Akú chemoterapiu chcete podať?
a)CapOx
b)CapIri
c)DDP/Gemcitabín
d)FOLFIRINOX\n """))

    if q=="a":
        Capox()
    elif q=="b":
        CapIri()
    elif q=="c":
        DDPGem()
    elif q=="d":
        FFRNX()
    else:
        print("\nzadaj a- d !!\n")
        chemorozc()


def bsa():
    global rbodysurf
    bodysurf= (w**0.425)*(h**0.725)*0.007184
    rbodysurf= round(bodysurf,2)
    print("""Telesný povrch je:""", rbodysurf,"""m2
                                          """)
    chemorozc()
    
def inpt():
    global w
    global h
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
            
           
    bsa()
    
print("""-------Vitajte v programe ChemoPy v1.1 !! -------------------
Program kedykoľvek ukončíte kombináciou CTRL-C """)
inpt()

    
