# MDM Colorectal

Nástroj **klinickej podpory rozhodovania** pre **kolorektálny karcinóm**. Na základe
postupne zadávaných klinicko-patologických atribútov (wizard) zobrazí štádium (AJCC TNM 8),
rizikovú stratifikáciu a odporúčaný terapeutický postup podľa **ESMO, NCCN a ASCO**.
Členené na klinické scenáre: **karcinóm kolon (st. I–III), karcinóm rekta (lokalizovaný)**
a **metastatický kolorektálny karcinóm (mCRC)**.

> ⚠️ **MDM Colorectal je nástroj vo vývoji.** Všetky odporúčania musia byť pred klinickým
> použitím overené oproti primárnym zdrojom. Nenahrádza klinický úsudok ani MDT.

Sesterská aplikácia k **MDM Gyn** a **MDM Mamma** — zdieľa rovnakú anti-halucinačnú
architektúru.

---

## Architektúra proti halucinácii

1. **Žiadny LLM pri runtime.** Aplikácia je čisto **deterministický matching engine**
   nad štruktúrovanou databázou (`kb/*.yaml`). Nikdy negeneruje klinický obsah za behu.
2. **Knowledge base je oddelená od kódu.** V `mdmcolorectal/` nie je žiadny klinický
   obsah — všetky kritériá aj odporúčania žijú v `kb/`.
3. **Každý záznam má povinné polia** (vynútené pydanticom v `mdmcolorectal/schema.py`):
   `society`, `guideline_version`, `year`, `source_reference`, `source_location`,
   `recommendation_text`, `reviewed`, `generated_by`, a pri overených `reviewed_by` +
   `reviewed_date`.
4. **`reviewed: false` = nepoužívať na klinické rozhodnutie.** Banner „⚠️ NEOVERENÉ“.
5. **Fallback:** ak pre kombináciu parametrov neexistuje záznam, appka to explicitne
   oznámi a odkáže na primárny zdroj — **nikdy nedopĺňa odhad.**
6. **Validačné testy** (`pytest`) zlyhajú pri chýbajúcom povinnom poli alebo ak `criteria`
   odkazuje na neznámy atribút/hodnotu.

### `reviewed` flag a stránka „Stav kontroly“

Každý záznam má `reviewed` (default `false`). Stránka **Stav kontroly** ukazuje počet
overených vs. neoverených záznamov per modul a spoločnosť. Prepnutie na `reviewed: true`
až po manuálnej kontrole oproti primárnemu zdroju (s vyplnením `reviewed_by` a
`reviewed_date`).

---

## Štruktúra

```
MDMColorectal/
├── app.py                 # Streamlit entry point
├── conftest.py
├── requirements.txt / requirements-dev.txt
├── .streamlit/config.toml
├── mdmcolorectal/        # KÓD — žiadny klinický obsah
│   ├── schema.py
│   ├── entities.py        # konfigurácia polí wizardu (nie klinický obsah)
│   ├── kb_loader.py
│   └── matching.py
├── kb/                   # ZNALOSTNÁ DATABÁZA (YAML) — klinický obsah
│   ├── colon.yaml
│   ├── rectum.yaml
│   └── metastatic.yaml
└── tests/
    ├── test_kb_validation.py
    └── test_matching.py
```

> Aktuálny obsah `kb/` sú **ilustračné seed záznamy (Fáza 1)** — všetky `reviewed: false`
> a `source_location: "NEOVERENÉ - doplniť"`.

---

## Lokálne spustenie

```bash
cd MDMColorectal
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
streamlit run app.py
```

Testy:

```bash
pytest -q
```

---

## Deploy na Streamlit Community Cloud

Súčasť repozitára `chemothon` v podadresári `MDMColorectal/`. Pri vytváraní Streamlit
Cloud appky nastav **Main file path** na `MDMColorectal/app.py`. Repozitár ponechaj
**private**, kým väčšina záznamov nie je `reviewed: true`.

---

## Žiadne PHI

Aplikácia neukladá žiadne pacientske dáta — pracuje len s abstraktnými klinickými
parametrami zadanými v rámci session.

---

## Fázy

1. **Fáza 1 (hotovo):** scaffold, schéma, wizard, „Stav kontroly“, validačné testy.
2. **Fáza 2:** naplnenie KB reálnym obsahom (offline; ideálne web search / primárne PDF).
3. **Fáza 3:** klinická kontrola a prepnutie na `reviewed: true`.
4. **Fáza 4:** rozšírenie pokrytia, CI validácia.
