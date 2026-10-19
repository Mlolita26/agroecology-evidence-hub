"""Copy the outcome directions out of the ontology, for build.py to read.

The ontology workbook (01_FOMD_ontologies.xlsx, sheet 01_outcomes) says for
each sub-indicator whether a higher value is good ('p') or bad ('n'). The
website needs that to say "did better" rather than "came out higher": a lower
cost is better, a lower pest count is better. build.py is standard library
only and cannot open a workbook, so this script writes the table it needs as
outcome_signs.csv next to build.py.

    python tools/fetch_outcome_signs.py

Run it again when the ontology changes. The workbook is opened read-only and
is never written to; that is the Hub's rule and this script keeps it.
"""

import csv
import glob
import io
import os

import openpyxl

HUB = os.path.expanduser(
    "~/OneDrive - CGIAR/Alliance-Agroecology Knowledge Hub - General/Agroecology_Evidence_Hub")
WEBSITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(WEBSITE, "outcome_signs.csv")


def main():
    matches = glob.glob(os.path.join(HUB, "02.FOMD", "02.metadata_structure", "01_FOMD_ontologies.xlsx"))
    if not matches:
        raise SystemExit("ontology workbook not found under " + HUB)
    book = openpyxl.load_workbook(matches[0], read_only=True, data_only=True)
    rows = list(book["01_outcomes"].iter_rows(values_only=True))
    head = [str(h).strip() if h is not None else "" for h in rows[0]]
    col = {name: head.index(name) for name in ("pillar", "subpillar", "indicator", "subindicator", "Sign")}

    table, blank = [], []
    for r in rows[1:]:
        if not r or r[col["subindicator"]] in (None, ""):
            continue
        sign = str(r[col["Sign"]] or "").strip().lower()
        sub = str(r[col["subindicator"]]).strip()
        if sign not in ("p", "n"):
            blank.append(sub)
            sign = ""
        table.append({
            "subindicator": sub, "sign": sign,
            "pillar": str(r[col["pillar"]] or "").strip(),
            "subpillar": str(r[col["subpillar"]] or "").strip(),
            "indicator": str(r[col["indicator"]] or "").strip(),
        })

    with io.open(OUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["subindicator", "sign", "pillar", "subpillar", "indicator"])
        writer.writeheader()
        writer.writerows(table)
    print(f"wrote {OUT}: {len(table)} sub-indicators, "
          f"{sum(1 for t in table if t['sign'] == 'p')} p, {sum(1 for t in table if t['sign'] == 'n')} n")
    if blank:
        print(f"{len(blank)} have no Sign in the ontology (build.py falls back to SIGN_FIXES for the ones in the data):")
        print("  " + "; ".join(blank))


if __name__ == "__main__":
    main()
