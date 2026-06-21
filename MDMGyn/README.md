# MDM Gyn

Nástroj **klinickej podpory rozhodovania** pre gynekologickú onkológiu. Na základe
postupne zadávaných klinicko-patologických atribútov (wizard) zobrazí FIGO štádium,
rizikovú stratifikáciu a odporúčaný terapeutický postup podľa **ESMO, ESGO, ESTRO a
NCCN**. Pokrýva 4 entity: **karcinóm endometria, cervixu, vulvy** a **nádory ovária/adnex**.

> ⚠️ **MDM Gyn je nástroj vo vývoji.** Všetky odporúčania musia byť pred klinickým
> použitím overené oproti primárnym zdrojom. Nenahrádza klinický úsudok ani MDT.

---

## Architektúra proti halucinácii

Toto je najdôležitejší princíp projektu:

1. **Žiadny LLM pri runtime.** Aplikácia je čisto **deterministický matching engine**
   nad štruktúrovanou databázou (`kb/*.yaml`). Nikdy negeneruje klinický obsah za behu.
2. **Knowledge base je oddelená od kódu.** V `mdmgyn/` nie je žiadny klinický obsah —
   všetky kritériá aj odporúčania žijú v `kb/`. Kód len páruje vstupy so záznamami.
3. **Každý záznam má povinné polia** (vynútené pydanticom v `mdmgyn/schema.py`):
   `society`, `guideline_version`, `year`, `source_reference`, `source_location`,
   `recommendation_text`, `reviewed`, `generated_by` (audit trail), a pri overených
   aj `reviewed_by` + `reviewed_date`.
4. **`reviewed: false` = nepoužívať na klinické rozhodnutie.** Takéto záznamy appka
   zobrazuje s výrazným bannerom „⚠️ AI-generovaný obsah, NEOVERENÉ“.
5. **Fallback:** ak pre kombináciu parametrov neexistuje záznam, appka explicitne
   oznámi „nie je odporúčanie — konzultuj primárny zdroj“ a **nikdy nedopĺňa odhad.**
6. **Validačné testy** (`pytest`) zlyhajú, ak ktorémukoľvek záznamu chýba povinné pole
   alebo ak `criteria` odkazuje na neznámy atribút/hodnotu.

### `reviewed` flag a stránka „Stav kontroly“

Každý záznam má `reviewed` (default `false`). Stránka **Stav kontroly** v appke ukazuje
počet overených vs. neoverených záznamov per entita a spoločnosť — slúži na sledovanie
priebehu kontroly pred prvým klinickým použitím. Záznam sa prepne na `reviewed: true`
až po manuálnej kontrole oproti primárnemu zdroju (vrátane vyplnenia `reviewed_by` a
`reviewed_date`).

---

## Štruktúra

```
MDMGyn/
├── app.py                 # Streamlit entry point
├── conftest.py            # pytest: cesta k balíku
├── requirements.txt       # runtime závislosti (pinnuté)
├── requirements-dev.txt   # + pytest
├── .streamlit/config.toml # UI nastavenia (žiadne secrets)
├── mdmgyn/                # KÓD — žiadny klinický obsah
│   ├── schema.py          # pydantic schéma KB záznamu
│   ├── entities.py        # konfigurácia polí wizardu (nie klinický obsah)
│   ├── kb_loader.py       # načítanie + tvrdá validácia KB
│   └── matching.py        # deterministický matching engine
├── kb/                   # ZNALOSTNÁ DATABÁZA (YAML) — klinický obsah
│   ├── endometrium.yaml
│   ├── cervix.yaml
│   ├── vulva.yaml
│   └── ovary.yaml
└── tests/
    ├── test_kb_validation.py
    └── test_matching.py
```

> Aktuálny obsah `kb/` sú **ilustračné seed záznamy (Fáza 1)** — všetky `reviewed: false`
> a `source_location: "NEOVERENÉ - doplniť"`. Vo Fáze 2 ich nahradí obsah z primárnych
> zdrojov, vo Fáze 3 sa overia.

---

## Lokálne spustenie

```bash
cd MDMGyn
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

Appka je súčasťou repozitára `chemothon` v podadresári `MDMGyn/`. Pri vytváraní
Streamlit Cloud appky nastav **Main file path** na `MDMGyn/app.py`. `app.py` si pridáva
vlastný adresár do `sys.path` a cesty ku KB rieši relatívne k `__file__`, takže funguje
nezávisle od pracovného adresára. Žiadne secrets nie sú potrebné. Repozitár ponechaj
**private**, kým väčšina záznamov nie je `reviewed: true`.

---

## Žiadne PHI

Aplikácia neukladá žiadne pacientske dáta — pracuje len s abstraktnými klinickými
parametrami zadanými v rámci session.

---

## Fázy

1. **Fáza 1 (hotovo):** scaffold, schéma, wizard, „Stav kontroly“, validačné testy,
   deploy-ready.
2. **Fáza 2:** naplnenie KB reálnym obsahom (offline, mimo runtime; ideálne web search /
   primárne PDF). Všetky nové záznamy `reviewed: false`.
3. **Fáza 3:** klinická kontrola cez „Stav kontroly“, prepnutie na `reviewed: true`.
4. **Fáza 4:** rozšírenie pokrytia, CI validácia.
