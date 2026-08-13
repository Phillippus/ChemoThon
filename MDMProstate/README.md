# MDM Prostata

Nástroj **klinickej podpory rozhodovania** pre **karcinóm prostaty**. Na základe
zadaných klinicko-patologických parametrov (cT, cN, cM, Gleason/Grade Group, PSA,
prípadne biopsia jadier a PSA denzita) zaradí pacienta do **NCCN rizikovej skupiny**:
Veľmi nízke, Nízke, Stredné (priaznivé/nepriaznivé), Vysoké, Veľmi vysoké riziko,
alebo Regionálne (N1) / Metastatické (M1).

> ⚠️ **MDM Prostata je nástroj vo vývoji.** Rizikové kritériá sú rekonštruované
> z pamäte a **NEOVERENÉ** oproti primárnemu zdroju (aktuálna verzia NCCN Prostate
> Cancer guideline). Pred klinickým použitím over hraničné hodnoty oproti PDF
> guideline. Nenahrádza klinický úsudok ani multidisciplinárny tím.

Sesterská aplikácia k **MDM Mamma / MDM Colorectal / MDM Gyn** — zdieľa rovnaký
princíp: žiadny LLM pri runtime, čisto deterministická logika.

---

## Architektúra proti halucinácii

1. **Žiadny LLM pri runtime.** Riziková skupina je vypočítaná čisto
   **deterministickou funkciou** (`mdmprostate/risk.py`) nad zadanými parametrami —
   žiadne generovanie textu za behu.
2. **Logika je oddelená od UI.** `mdmprostate/risk.py` neobsahuje žiadny Streamlit
   kód a je plne pokrytá testami (`tests/test_risk.py`).
3. **Explicitné caveaty namiesto tichých predpokladov.** Ak používateľ nezadá
   voliteľný parameter potrebný na potvrdenie/vylúčenie podkritéria (napr. podiel
   pozitívnych jadier pri nepriaznivom strednom riziku), appka to vypíše ako
   varovanie namiesto toho, aby ticho predpokladala "nesplnené".
4. **Zdroj je označený ako neoverený**, kým ho niekto manuálne neskontroluje
   oproti aktuálnej verzii NCCN guideline (mení sa niekoľkokrát ročne).
5. Žiadne PHI/pacientske dáta sa neukladajú — appka pracuje len s abstraktnými
   klinickými parametrami v rámci session.

## Rozsah / mimo rozsahu

- **Pokrýva:** zaradenie do NCCN rizikovej skupiny pre klinicky lokalizovaný a
  lokálne pokročilý karcinóm prostaty (cT1a–T4, N0–N1, M0–M1).
- **Nepokrýva:** terapeutické odporúčania, nomogramy (CAPRA, MSKCC, Partin
  tabuľky), kastračne rezistentné ochorenie, molekulárne testovanie (Decipher,
  Oncotype DX).

## Spustenie

```bash
pip install -r requirements-dev.txt
streamlit run app.py
```

## Testy

```bash
pytest
```

## Prioritný TODO pred klinickým použitím

- [ ] Manuálne overiť všetky hraničné hodnoty (PSA 10/20, ≤50 % jadro, PSA
      denzita 0.15, >4 jadrá GG4–5, ...) oproti aktuálnej verzii NCCN guideline
      a doplniť presné číslo verzie/roku do `mdmprostate/risk.py`.
- [ ] Zvážiť pridanie warningu, ak zadaná kombinácia T/N/M je klinicky
      nekonzistentná (napr. T4 s N0 M0 je možné, ale stojí za dvojité overenie).
