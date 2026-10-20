"""Explore HEASARC TAP catalog schema; don't combine data without validating provenance."""
from io import BytesIO
import requests
from astropy.table import Table
ENDPOINT="https://heasarc.gsfc.nasa.gov/xamin/vo/tap/sync"
def tap(query):
    r=requests.get(ENDPOINT,params={"REQUEST":"doQuery","LANG":"ADQL","QUERY":query,"FORMAT":"votable"},timeout=60)
    r.raise_for_status()
    return Table.read(BytesIO(r.content),format="votable")
if __name__=="__main__":
    tables=tap("SELECT TOP 100 table_name, description FROM tap_schema.tables")
    names=[str(x).lower() for x in tables["table_name"]]
    matches=[x for x in names if any(k in x for k in ("bh", "black", "swift", "maxi", "xrb", "transient"))]
    print("Potential tables (verify catalog schema/provenance):", matches)
    print("This discovery script imports no source measurements automatically.")
