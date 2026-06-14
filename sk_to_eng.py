"""
Translation utility: common Slovak medical abbreviations → English.
Used by all ChemoThon ENG apps to translate content from individual JSON files.
"""
import re


def sk_to_eng(text: str) -> str:
    """Translate common Slovak medical terms/abbreviations to English."""
    if not text:
        return text

    # --- Drug / brand name corrections ---
    text = text.replace("Dexametazon", "Dexamethasone")
    text = text.replace("Dexametazón", "Dexamethasone")
    text = text.replace("Nolpaza", "Pantoprazole")
    text = text.replace("Pantoprazol ", "Pantoprazole ")
    text = text.replace("Pantoprazol.", "Pantoprazole.")
    text = text.replace("Pantoprazol,", "Pantoprazole,")
    text = text.replace("Hydrocortison", "Hydrocortisone")
    text = text.replace("Dithiaden", "Chlorphenamine")
    text = text.replace("Bisulepin", "Chlorphenamine")
    text = text.replace("Ondasetron", "Ondansetron")
    text = text.replace("pegfilgrastim", "pegfilgrastim")   # same
    text = text.replace("lipegfilgrastim", "lipegfilgrastim")  # same

    # --- Route / form ---
    text = text.replace("i.v.", "iv").replace("i. v.", "iv")
    text = text.replace(" tbl p.o.", " tab p.o.")
    text = text.replace(" tbl.", " tab.")
    text = text.replace(" tbl ", " tab ")
    text = text.replace(" tbl,", " tab,")

    # --- Solution abbreviations (whole-word) ---
    # FR = Fyziologický Roztok = Normal Saline
    text = re.sub(r'\bFR\b', 'NS', text)
    # RR = Ringer's Roztok
    text = re.sub(r'\bRR\b', "Ringer's", text)
    # G 5%  (glucose) — already recognisable, keep as is

    # --- "v Xml" → "in Xml" (Slovak preposition "v" = English "in") ---
    text = re.sub(r'^v\s+(\d)', r'in \1', text)
    text = re.sub(r'([\s,;/])v\s+(\d)', r'\1in \2', text)

    # --- Infusion schedule phrases ---
    text = text.replace("1.infuzia:", "1st infusion:")
    text = text.replace("1. infuzia:", "1st infusion:")
    text = text.replace("1.infúzia:", "1st infusion:")
    text = text.replace("1. infúzia:", "1st infusion:")
    text = text.replace("infuzia", "infusion")
    text = text.replace("infúzia", "infusion")
    text = text.replace("zacat 50ml/h", "start at 50 ml/h")
    text = text.replace("zacat 50 ml/h", "start at 50 ml/h")
    text = text.replace("začat 50ml/h", "start at 50 ml/h")
    text = text.replace("stupnovite zvysovat", "escalate gradually")
    text = text.replace("stupňovito zvyšovať", "escalate gradually")
    text = text.replace("dalsie cykly:", "subsequent cycles:")
    text = text.replace("dalsie cykly", "subsequent cycles")
    text = text.replace("ďalšie cykly:", "subsequent cycles:")
    text = text.replace("ďalšie cykly", "subsequent cycles")
    text = text.replace("ďalšie:", "subsequent:")
    text = text.replace("ďalšie ", "subsequent ")

    # --- Time ---
    text = re.sub(r'(\d+)\s*hodín', r'\1 hours', text)
    text = re.sub(r'(\d+)\s*hod\b', r'\1 h', text)
    text = text.replace("24hod", "24 h")

    # --- Administration site ---
    text = text.replace("centralny kateter", "central catheter")
    text = text.replace("centrálny katéter", "central catheter")

    # --- Scheduling/frequency ---
    text = text.replace("ráno a večer", "morning and evening")
    text = text.replace("každé 3 týždne", "every 3 weeks")
    text = text.replace("každé 4 týždne", "every 4 weeks")
    text = text.replace("každý týždeň", "every week")
    text = text.replace("každých", "every")
    text = text.replace("každé", "every")
    text = text.replace("denne", "daily")
    text = text.replace("do 2 rokov", "for up to 2 years")
    text = text.replace("týždne", "weeks")
    text = text.replace("týždeň", "week")
    text = text.replace("mesiacov", "months")
    text = text.replace("mesiac", "month")
    text = text.replace("rozostupy", "intervals")
    text = re.sub(r'\bcyklov\b', 'cycles', text)

    # --- Day connectors ---
    text = re.sub(r'\bD(\d+)\s+a\s+D(\d+)', r'D\1 and D\2', text)
    text = text.replace("po dotečení posledného dňa", "after the last-day infusion completes")

    # --- Clinical notes ---
    text = text.replace("Bez premedikácie.", "No premedication.")
    text = text.replace("Bez premedikácie", "No premedication")
    text = text.replace("POVINNÁ B12/FOLÁT suplementácia", "MANDATORY B12/FOLATE supplementation")
    text = text.replace("POVINNÁ", "MANDATORY")
    text = text.replace("suplementácia", "supplementation")
    text = text.replace("Redukcia pri", "Dose reduction at")
    text = text.replace("Premedikácia", "Premedication")
    text = text.replace("premedikácia", "premedication")
    text = text.replace("Udržiavacia liečba:", "Maintenance therapy:")
    text = text.replace("Udržiavacia liečba", "Maintenance therapy")
    text = text.replace("Indikácia:", "Indication:")
    text = text.replace("Indikácia", "Indication")
    text = text.replace("neskvamózny NSCLC", "non-squamous NSCLC")
    text = text.replace("skvamózny NSCLC", "squamous NSCLC")
    text = text.replace("Vincristín VYNECHANÝ", "Vincristine OMITTED")
    text = text.replace("VYNECHANÝ", "OMITTED")
    text = text.replace("línia", "line")
    text = text.replace("linia", "line")
    text = text.replace("viď", "see")
    text = text.replace("pred.", "prior.")
    text = text.replace("sc", "sc")  # subcut — same

    return text
