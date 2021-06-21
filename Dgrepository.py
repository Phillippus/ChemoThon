
def hematology(rbodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane v hematoonkologii"""
    hem=str(input("""Aku chemoterapiu chcete podat?  
a) ABVD
b) R-CHOP
c) miniCHOP
d) CVP
e) DHAP
f) GemOx\n"""))
    
    if hem=="a":
        ABVD()
    elif hem=="b":
        RCHOP()
    elif hem=="c":
        MCHOP()
    elif hem=="d":
        CVP()
    elif hem=="e":
        DHAP()
    elif hem=="f":
        GemOx()
   
    else:
        print("""Musite zadat a-f!""")
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
i) palbociclib\n"""))
    
    if brs=="a":
    	EC()
    elif brs=="b":
        AC()
    elif brs=="c":
        ddAC()
    elif brs=="d":
        docetaxel()
    elif brs=="e":
        paclitaxel()
    elif brs=="f":
        capecitabin()
    elif brs=="g":
        gemcitabin()
    elif brs=="h":
      	ribociclib()
    elif brs=="i":
        palbociclib()
    else:
        print("""Musite zadat a-i!""")
        breast(rbodysurf)
        
def lung(rbodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane v liecbe karcinomu pluc"""
    lng=str(input("""Aku chemoterapiu chcete podat?  
a) CBDCA/ gemcitabin
b) CBDCA/ pemetrexed
c) CBDCA/ paclitaxel
d) Docetaxel
e) Vinorelbin adjuvant
f) Vinorelbin paliative
g) DDP/ Etoposid
h) Topotecan + G-CSF\n"""))
    
    if lng=="a":
    	CBGem()
    elif lng=="b":
        CBPem()
    elif lng=="c":
        CBpcl()
    elif lng=="d":
        docetaxel()
    elif lng=="e":
        vnradj()
    elif lng=="f":
        vnrpal()
    elif lng=="g":
        DDPEto()
    elif lng=="h":
      	Topotecan()

    else:
        print("""Musite zadat a-h!""")
        lung(rbodysurf)

def colorectal(bodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane 
    v liecbe kolorektalneho karcinomu"""
    crc=str(input("""Aku chemoterapiu chcete podat?  
a) CapOx
b) CapIri
c) FOLFOX
d) FOLFIRI
e) mFOLFIRINOX
f) capecitabin
g) trifluridine/tipiracil
h) bevacizumab 14d
i) bevacizumab 21d
j) cetuximab
k) panitumumab\n"""))
    
    if crc=="a":
        CapOx()
    elif crc=="b":
        CapIri()
    elif crc=="c":
        FOLFOX()
    elif crc=="d":
        FOLFIRI()
    elif crc=="e":
        FOLFIRINOX()
    elif crc=="f":
        capecitabin()
    elif crc=="g":
        triti()
    elif crc=="h":
      	bev2w()
    elif crc=="i":
        bev3w()
    elif crc=="j":
        cetux()
    elif crc=="k":
        panitum()

    else:
        print("""Musite zadat a-k!""")
        colorectal(bodysurf)

def git(rbodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane 
    v liecbe malignít GITu"""
    gt=str(input("""Aku chemoterapiu chcete podat?  
a) DDP/ 5-FU
b) FLOT
c) EOX
d) paclitaxel weekly
e) irinotecan
e) mFOLFIRINOX
f) gemcitabin/ capecitabin
g) gemcitabin/ nab- paclitaxel
h) DDP/ gemcitabin
i) Mitomycin/ 5-FU
j) ramucirumab\n"""))
    
    if gt=="a":
        DDP5FU()
    elif gt=="b":
        FLOT()
    elif gt=="c":
        EOX()
    elif gt=="d":
        paclitaxel()
    elif gt=="e":
        FOLFIRINOX()
    elif gt=="f":
        gemcap()
    elif gt=="g":
        gemnabpcl()
    elif gt=="h":
      	DDPGem()
    elif gt=="i":
        bev3w()
    elif crc=="j":
        MTC5FU()
    elif gt=="k":
        ramucirumab()

    else:
        print("""Musite zadat a-k!""")
        git(rbodysurf)
        
def headandneck(rbodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane 
    v liecbe malignít hlavy a krku"""
    han=str(input("""Aku chemoterapiu chcete podat?  
a) DDP/ 5-FU
b) paclitaxel weekly
c) metotrexat weekly
d) DCF\n"""))
    
    if han=="a":
        DDP5FU()
    elif han=="b":
        paclitaxel()
    elif han=="c":
        MTX()
    elif han=="d":
        DCF()
    
    else:
        print("""Musite zadat a-d!""")
        headandneck(rbodysurf)
        
def sarcoma(bodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane 
    v liecbe sarkomov, GISTomov, neuromalignit a melanomu"""
    sar=str(input("""Aku chemoterapiu chcete podat?  
a) Doxorubicin/ ifosfamid
b) Epirubicin/ ifosfamid
c) ifosfamid
d) trabectedin
e) pazopanib
f) gemcitabin/ docetaxel
g) imatinib
h) sunitinib
i) dabrafenib/ trametinib
j) cobimetinib/ vemurafenib
k) dacarbazin
l) temozolomid/ RAT
m) temozolomid/ solo\n"""))
    
    if sar=="a":
        DoxIfo()
    elif sar=="b":
        EpiIfo()
    elif sar=="c":
        Ifo()
    elif sar=="d":
        trabectedin()
    elif sar=="e":
        pazopanib()
    elif sar=="f":
        gemdoc()
    elif sar=="g":
        imatinib()
    elif sar=="h":
        sunitinib()
    elif sar=="i":
        dabratrame()
    elif sar=="j":
        cobivemu()
    elif sar=="k":
        dacarbazin()
    elif sar=="l":
        temoRAT()
    elif sar=="m":
        temoSOLO()
    
    
    else:
        print("""Musite zadat a-m!""")
        sarcoma(bodysurf)

def prostate(rbodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane 
    v liecbe karcinomu prostaty"""
    prst=str(input("""Aku chemoterapiu chcete podat?  
a) docetaxel/ prednison
b) cabazitaxel/ prednison
c) abirateron/ prednison
d) enzalutamid\n"""))
    
    if prst=="a":
        DocPrd()
    elif prst=="b":
        CabPrd()
    elif prst=="c":
        AbirPrd()
    elif prst=="d":
        enzalutamid()
    
    else:
        print("""Musite zadat a-d!""")
        prostate(rbodysurf)
        
def urogenital(rbodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane 
    v liecbe urogenitalnych malignit"""
    urol=str(input("""Aku chemoterapiu chcete podat?  
a) DDP/Gemcitabin
b) vinflunin
c) TIP
d) DDP/5-FU
e) pazopanib
f) sunitinib
g) nivolumab
h) BEP\n"""))
    
    if urol=="a":
        DDPGem()
    elif urol=="b":
        vinflunin()
    elif urol=="c":
        TIP()
    elif urol=="d":
        DDP5FU()
    elif urol=="e":
        pazopanib()
    elif urol=="f":
        sunitinib()
    elif urol=="g":
        nivolumab()
    elif urol=="h":
        BEP()
    
    else:
        print("""Musite zadat a-h!""")
        urogenital(rbodysurf)

def gynecology(rbodysurf):
    """Tato funkcia ponuka chemoterapie pouzivane 
    v liecbe gynekologických malignít"""
    gynec=str(input("""Aku chemoterapiu chcete podat?  
a) CBDCA/paclitaxel
b) CBDCA/ paclitaxel/ bevacizumab
c) topotecan
d) olaparib\n"""))
    
    if gynec=="a":
        CBpcl()
    elif gynec=="b":
        CBpclbev()
    elif gynec=="c":
        Topotecan()
    elif gynec=="d":
        olaparib()
    
    else:
        print("""Musite zadat a-d!""")
        gynecology(rbodysurf)
        
def immunotherapy(rbodysurf):
    """Tato funkcia ponuka moznosti imunoterapie"""
    immuno=str(input("""Aku imunoterapiu chcete podat?  
a) pembrolizumab
b) nivolumab
c) avelumab\n"""))
    
    if immuno=="a":
        pembrolizumab()
    elif immuno=="b":
        nivolumab()
    elif immuno=="c":
        avelumab()
   
    else:
        print("""Musite zadat a-c!""")
        immunotherapy(rbodysurf)