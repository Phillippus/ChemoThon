# MDM Haematology

Nástroj **klinickej podpory rozhodovania** pre **lymfómy** (NIE leukémie). Na základe
postupne zadávaných klinicko-patologických atribútov (wizard) zobrazí štádium (Lugano /
Ann Arbor), rizikovú stratifikáciu a odporúčaný terapeutický postup podľa **ESMO, NCCN
a EHA**.

Moduly (typy lymfómov):
- **Hodgkinov lymfóm (klasický)**
- **DLBCL** — difúzny veľkobunkový B-lymfóm
- **Folikulárny lymfóm (FL)**
- **Lymfóm z plášťových buniek (MCL)**
- **Marginálnozónový lymfóm (MZL)**
- **Periférny T-bunkový lymfóm (PTCL)**

> ⚠️ **MDM Haematology je nástroj vo vývoji.** Všetky odporúčania musia byť pred klinickým
> použitím overené oproti primárnym zdrojom. Nenahrádza klinický úsudok ani MDT.

Sesterská aplikácia k **MDM Gyn**, **MDM Mamma** a **MDM Colorectal** — zdieľa rovnakú
anti-halucinačnú architektúru.

---

## Architektúra proti halucinácii

1. **Žiadny LLM pri runtime.** Aplikácia je čisto **deterministický matching engine**
   nad štruktúrovanou databázou (`kb/*.yaml`). Nikdy negeneruje klinický obsah za behu.
2. **Knowledge base je oddelená od kódu.** V `mdmhaematology/` nie je žiadny klinický
   obsah — všetky kritériá aj odporúčania žijú v `kb/`.
3. **Prognostické indexy (IPI/FLIPI/MIPI/IPS) sa NEPOČÍTAJÚ** — zadávajú sa ako vstup.
   Appka nič nevyhodnocuje, len páruje so záznamami KB.
4. **Každý záznam má povinné polia** (vynútené pydanticom v `mdmhaematology/schema.py`):
   `society`, `guideline_version`, `year`, `source_reference`, `source_location`,
   `recommendation_text`, `reviewed`, `generated_by`, a pri overených `reviewed_by` +
   `reviewed_date`.
5. **`reviewed: false` = nepoužívať na klinické rozhodnutie.** Banner „⚠️ NEOVERENÉ“.
6. **Fallback:** ak pre kombináciu parametrov neexistuje záznam, appka to explicitne
   oznámi a odkáže na primárny zdroj — **nikdy nedopĺňa odhad.**
7. **Validačné testy** (`pytest`) zlyhajú pri chýbajúcom povinnom poli alebo ak `criteria`
   odkazuje na neznámy atribút/hodnotu.

### `reviewed` flag a stránka „Stav kontroly“

Každý záznam má `reviewed` (default `false`). Stránka **Stav kontroly** ukazuje počet
overených vs. neoverených záznamov per modul a spoločnosť. Prepnutie na `reviewed: true`
až po manuálnej kontrole oproti primárnemu zdroju (s vyplnením `reviewed_by` a
`reviewed_date`).

---

## Štruktúra

```
MDMHaematology/
├── app.py                 # Streamlit entry point
├── conftest.py
├── requirements.txt / requirements-dev.txt
├── .streamlit/config.toml
├── mdmhaematology/       # KÓD — žiadny klinický obsah
│   ├── schema.py
│   ├── entities.py        # konfigurácia polí wizardu (nie klinický obsah)
│   ├── kb_loader.py
│   └── matching.py
├── kb/                   # ZNALOSTNÁ DATABÁZA (YAML) — klinický obsah
│   ├── hl.yaml
│   ├── dlbcl.yaml
│   ├── fl.yaml
│   ├── mcl.yaml
│   ├── mzl.yaml
│   └── ptcl.yaml
└── tests/
    ├── test_kb_validation.py
    └── test_matching.py
```

> Aktuálny obsah `kb/` sú **ilustračné seed záznamy (Fáza 1)** — všetky `reviewed: false`
> a `source_location: "NEOVERENÉ - doplniť"`.

---

## Lokálne spustenie

```bash
cd MDMHaematology
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

Súčasť repozitára `chemothon` v podadresári `MDMHaematology/`. Pri vytváraní Streamlit
Cloud appky nastav **Main file path** na `MDMHaematology/app.py`. Repozitár ponechaj
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
4. **Fáza 4:** rozšírenie pokrytia (ďalšie podtypy, relaps/refraktérne línie), CI validácia.
