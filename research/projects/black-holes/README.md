# Černé díry — výzkumný projekt

## První datový produkt

Tento projekt začíná reprodukovatelným snapshotem veřejného katalogu gravitačních vln GWOSC/GWTC. Katalog popisuje detekované kompaktní binární události, z nichž mnohé jsou sloučení černých děr. Nezaměňovat katalogové události za všechny známé černé díry nebo za realtime observatoř.

Aktualizace (vyžaduje síť):

```bash
cd ~/Projects/astro-science
.venv/bin/python research/projects/black-holes/scripts/update_gwosc.py
```

Výstupy: SQLite `data/black_holes.sqlite`, report `reports/latest.md`, grafy `figures/`. Tabulka `fetch_log` uchovává čas každého stažení; data ukládají čas stažení, event GPS, katalog a URL. Skript nahrazuje aktuální tabulku katalogovým snapshotem, proto před každým přepsáním zálohujte DB, pokud potřebujete historickou verzi tabulky. Report je průzkumný, ne odborný závěr.

## Zdroje a odkazy

- GWOSC API: https://gwosc.org/api/ — veřejné read-only rozhraní, bez autentizace; API v2 katalogy/eventy a strain data.
- GWOSC event API v1 používaný skriptem: https://gwosc.org/eventapi/json/GWTC/ — rychlý JSON snapshot; přejít na v2 po ověření schématu/paginace.
- HEASARC: https://heasarc.gsfc.nasa.gov/ — high-energy mission archives; TAP/VO queries, např. Xamin TAP service. Výběr tabulky a query je potřeba validovat dle konkrétního katalogu.
- NASA Exoplanet Archive není black-hole katalog (nepoužívat jako zdroj BH měření).
- ADS bibliografické API: https://ui.adsabs.harvard.edu/ — API klíč nutný pro vyhledávání.

## Otázky výzkumu, které vyžadují další specifikaci

Vyber hlavní směr: (1) populace gravitačních vln a hmotnostní/spinové rozdělení, (2) rentgenové dvojhvězdy a akrece, (3) supermasivní černé díry/AGN, (4) multimessenger a historické flare události. „Live data“ musí mít definovaný zdroj, kadenci a význam času; mnoho veřejných vědeckých katalogů je aktualizováno po vydání, nikoli kontinuálně.

## Další software

Nainstalováno do stávající `.venv`: `gwosc` (katalogy/metadata) a `gwpy` (strain a analýza gravitačních vln). `lalsuite` a SXS tooling zatím nejsou nainstalované; LALSuite je velký nativní stack a současná venv používá Python 3.14, proto nejdřív ověřit kompatibilitu v odděleném prostředí, než riskovat existující astrofyzikální setup.
