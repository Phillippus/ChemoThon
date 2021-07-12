def ifosfamide(rbodysurf,dose, otherCHT):
    ifo=int(dose*rbodysurf)
    mesna=ifo*0.8
    ifocycle=ifo//2000
    mesnacycle=ifocycle+1
    iforemnant=ifo%2000
    mesnainit=1200
    mesnaend=800
    
    
    
    if otherCHT==True:
        print("""epirubicin 60mg/m2........""",60*rbodysurf,"""mg D1, D2
ifosfamid 3000mg/m2..........""",ifo,"""mg D1,D2,D3
mesna 0.8 x ifosfamid........""",mesna,"""mg D1,D2,D3
              
                                        NC 21. den
                                                        
                                                        D1
                                                            """)
        
        print("""Ondasetron 8mg iv, Dexametazon 8mg iv, Pantoprazol 40mg p.o.""")
        print("""Epirubicin""",60*rbodysurf,"""mg v 500ml FR iv""")
        print("""MESNA""",mesnainit,"""mg v 100ml FR /4hodiny""")
        if iforemnant>200:
            mesnacont=(mesna-2000)//ifocycle
            for cycifo in range(0,ifocycle):
                print("""Ifosfamid 2000mg v 500ml FR iv""")
                print("""MESNA""",mesnacont,"""mg v 100ml FR iv/ 4 hodiny""")
            print("""Ifosfamid""",iforemnant,"""mg 500ml FR iv""")
            print("""MESNA 800mg v 100ml FR iv/ 4 hodiny""")   
        else: 
            mesnacont=(mesna-1200)//ifocycle
            for cycifo in range(0,ifocycle):
                print("""Ifosfamid 2000mg v 500ml FR iv""")
                print("""MESNA""",mesnacont,"""mg v 100ml FR iv/ 4 hodiny""")
    
   
   
    else:
        print("""ifosfamid 3000mg/m2..........""",ifo,"""mg D1,D2,D3
mesna 0.8 x ifosfamid........""",mesna,"""mg D1,D2,D3
              
                                        NC 21. den
                                                        
                                                        D1
                                                            """)
        
        print("""Ondasetron 8mg iv, Dexametazon 8mg iv, Pantoprazol 40mg p.o.""")
        print("""MESNA""",mesnainit,"""mg v 100ml FR /4hodiny""")
        if iforemnant>200:
            mesnacont=(mesna-2000)//ifocycle
            for cycifo in range(0,ifocycle):
                print("""Ifosfamid 2000mg v 500ml FR iv""")
                print("""MESNA""",mesnacont,"""mg v 100ml FR iv/ 4 hodiny""")
            print("""Ifosfamid""",iforemnant,"""mg 500ml FR iv""")
            print("""MESNA 800mg v 100ml FR iv/ 4 hodiny""")   
        else: 
            mesnacont=(mesna-1200)//ifocycle
            for cycifo in range(0,ifocycle):
                print("""Ifosfamid 2000mg v 500ml FR iv""")
                print("""MESNA""",mesnacont,"""mg v 100ml FR iv/ 4 hodiny""")
             
        
        
ifosfamide(2.1,3000,True)