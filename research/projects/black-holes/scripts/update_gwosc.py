#!/usr/bin/env python3
"""Fetch public GWOSC compact-binary event catalog and make a local snapshot/report."""
from datetime import datetime, timezone
from pathlib import Path
import json, sqlite3
import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "black_holes.sqlite"
OUT = ROOT / "reports"
FIG = ROOT / "figures"
API = "https://gwosc.org/eventapi/json/GWTC/"

def main():
    fetched = datetime.now(timezone.utc).isoformat()
    response = requests.get(API, timeout=45, headers={"User-Agent":"astro-science-black-hole-research/1.0"})
    response.raise_for_status()
    events = response.json().get("events", {})
    if not events:
        raise RuntimeError("GWOSC response contained no events")
    rows=[]
    for key,e in events.items():
        rows.append({"event_id":e.get("commonName",key), "version":e.get("version"), "catalog":e.get("catalog.shortName"),
        "gps":e.get("GPS"), "mass_1_source_msun":e.get("mass_1_source"), "mass_2_source_msun":e.get("mass_2_source"),
        "total_mass_source_msun":e.get("total_mass_source"), "chirp_mass_source_msun":e.get("chirp_mass_source"),
        "final_mass_source_msun":e.get("final_mass_source"), "luminosity_distance_mpc":e.get("luminosity_distance"),
        "redshift":e.get("redshift"), "chi_eff":e.get("chi_eff"), "network_snr":e.get("network_matched_filter_snr"),
        "far_per_year":e.get("far"), "p_astro":e.get("p_astro"), "source_url":e.get("jsonurl"), "fetched_utc":fetched})
    df=pd.DataFrame(rows).drop_duplicates(["event_id","version"])
    OUT.mkdir(parents=True,exist_ok=True); FIG.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(DB) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS gwtc_events (
            event_id TEXT, version INTEGER, catalog TEXT, gps REAL, mass_1_source_msun REAL, mass_2_source_msun REAL,
            total_mass_source_msun REAL, chirp_mass_source_msun REAL, final_mass_source_msun REAL,
            luminosity_distance_mpc REAL, redshift REAL, chi_eff REAL, network_snr REAL, far_per_year REAL,
            p_astro REAL, source_url TEXT, fetched_utc TEXT, UNIQUE(event_id,version,fetched_utc))""")
        df.to_sql("_incoming",con,if_exists="replace",index=False)
        cols=", ".join(df.columns)
        con.execute(f"INSERT OR IGNORE INTO gwtc_events ({cols}) SELECT {cols} FROM _incoming")
        con.execute("DROP TABLE _incoming")
        con.execute("CREATE TABLE IF NOT EXISTS fetch_log (fetched_utc TEXT, source TEXT, row_count INTEGER, http_status INTEGER)")
        con.execute("INSERT INTO fetch_log VALUES (?,?,?,?)",(fetched,API,len(df),response.status_code))
    valid=df.dropna(subset=["total_mass_source_msun"])
    fig,ax=plt.subplots(figsize=(9,5));
    if len(valid):
        ax.hist(valid.total_mass_source_msun,bins=min(25,max(5,int(len(valid)**.5))),color="#335c99",edgecolor="white")
        ax.set_xlabel("Source-frame total mass (solar masses)"); ax.set_ylabel("Catalog events")
    else: ax.text(.5,.5,"Mass estimates not populated in this catalog response",ha="center",va="center",transform=ax.transAxes)
    ax.set_title("GWOSC compact-binary detections: source-frame total mass")
    fig.tight_layout(); fig.savefig(FIG/"gwtc_total_mass.png",dpi=160); plt.close(fig)
    snr=df.dropna(subset=["network_snr"])
    fig,ax=plt.subplots(figsize=(9,5))
    if len(snr):
        ax.scatter(range(len(snr)),snr.network_snr,s=16,alpha=.7); ax.set_ylabel("Network matched-filter SNR"); ax.set_xlabel("Events (catalog order)")
    ax.set_title("GWOSC event-catalog network SNR"); fig.tight_layout(); fig.savefig(FIG/"gwtc_snr.png",dpi=160); plt.close(fig)
    report=["# Černé díry – automatický katalogový přehled", "", f"Aktualizováno UTC: {fetched}",
      f"Zdroj: [GWOSC GWTC event API]({API}) (veřejná služba, bez autentizace).",f"Záznamů ve snapshotu: {len(df)}.",
      "", "## Co data znamenají", "GWOSC GWTC obsahuje katalog gravitačně-vlnových přechodových událostí, převážně sloučení kompaktních dvojic. Nejde o přímý nepřetržitý přenos: jde o veřejný katalog publikovaných/aktualizovaných událostí. `fetched_utc` je čas stažení; `gps` je čas události. Některé parametry mohou být v katalogovém endpointu prázdné; nejistoty a posteriorní vzorky je nutné načítat z detailních produktů jednotlivých událostí.",
      "", "## Grafy", "- `../figures/gwtc_total_mass.png` – histogram jen tam, kde je hmotnost dostupná.", "- `../figures/gwtc_snr.png` – síťové SNR katalogových událostí.",
      "", "## Databáze", "SQLite `../data/black_holes.sqlite`, tabulka `gwtc_events` (surové klíčové parametry a zdroj) a `fetch_log` (čas a počet záznamů). Tento zdroj je gravitačně-vlnový katalog; neobsahuje všechny známé černé díry ani průběžné elektromagnetické monitorování.",
      "", "## Omezení a další kroky", "Hmotnosti jsou v solárních hmotnostech, vzdálenosti v Mpc dle metadat GWOSC. Nepovažujte chybějící hodnotu za nulu. Pro reprodukovatelné vědecké závěry je potřeba zachovat release/version, dohledat paper/DOI, intervaly nejistot a výběrové efekty. Další rozšíření: HEASARC/Swift-XRT, MAXI, NICER a NASA ADS bibliografie; live X-ray provozní telemetrie nemusí být veřejná/API dostupná.",
      ""]
    (OUT/"latest.md").write_text("\n".join(report))
    print(f"Updated {len(df)} events; database={DB}; report={OUT/'latest.md'}")
if __name__ == "__main__": main()
