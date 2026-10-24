# Černé díry – automatický katalogový přehled

Aktualizováno UTC: 2026-10-24T20:19:51.537146+00:00
Zdroj: [GWOSC GWTC event API](https://gwosc.org/eventapi/json/GWTC/) (veřejná služba, bez autentizace).
Záznamů ve snapshotu: 391.

## Co data znamenají
GWOSC GWTC obsahuje katalog gravitačně-vlnových přechodových událostí, převážně sloučení kompaktních dvojic. Nejde o přímý nepřetržitý přenos: jde o veřejný katalog publikovaných/aktualizovaných událostí. `fetched_utc` je čas stažení; `gps` je čas události. Některé parametry mohou být v katalogovém endpointu prázdné; nejistoty a posteriorní vzorky je nutné načítat z detailních produktů jednotlivých událostí.

## Grafy
- `../figures/gwtc_total_mass.png` – histogram jen tam, kde je hmotnost dostupná.
- `../figures/gwtc_snr.png` – síťové SNR katalogových událostí.

## Databáze
SQLite `../data/black_holes.sqlite`, tabulka `gwtc_events` (surové klíčové parametry a zdroj) a `fetch_log` (čas a počet záznamů). Tento zdroj je gravitačně-vlnový katalog; neobsahuje všechny známé černé díry ani průběžné elektromagnetické monitorování.

## Omezení a další kroky
Hmotnosti jsou v solárních hmotnostech, vzdálenosti v Mpc dle metadat GWOSC. Nepovažujte chybějící hodnotu za nulu. Pro reprodukovatelné vědecké závěry je potřeba zachovat release/version, dohledat paper/DOI, intervaly nejistot a výběrové efekty. Další rozšíření: HEASARC/Swift-XRT, MAXI, NICER a NASA ADS bibliografie; live X-ray provozní telemetrie nemusí být veřejná/API dostupná.
