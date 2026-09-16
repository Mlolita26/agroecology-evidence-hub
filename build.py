"""Build the website dataset from the harmonised 10_ schema effect-size tables.

Reads every CSV in the clean effect-size folder, turns each control-vs-treatment
comparison into one website record, and writes docs/data.js.

    python build.py

Set SOURCE_DIR below if your copy of the Hub lives somewhere else.
"""

import csv
import glob
import json
import math
import os
import re

SOURCE_DIR = os.path.expanduser(
    "~/OneDrive - CGIAR/Alliance-Agroecology Knowledge Hub - General"
    "/Agroecology_Evidence_Hub/02.FOMD/04.metadata_effectsize/03.fomd10_clean"
)
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

# The source has no region column, and the vocabulary is small enough to list.
REGIONS = {
    "Colombia": "South America",
    "Ethiopia": "Eastern Africa",
    "Guatemala": "Central America",
    "India": "Southern Asia",
    "Kenya": "Eastern Africa",
    "Malawi": "Southern Africa",
    "Mexico": "Central America",
    "Peru": "South America",
    "South Africa": "Southern Africa",
    "Tunisia": "Northern Africa",
    "Vietnam": "South-eastern Asia",
    "Zambia": "Southern Africa",
}

# Practice themes, in the order we prefer them. The first theme whose two sides
# differ is the contrast the record is about.
THEMES = [
    "variety_management",
    "breed_animal",
    "planting_management",
    "diversification_spatial",
    "diversification_temporal",
    "soil_management",
    "nutrient_management",
    "pest_management",
    "water_management",
    "biomass_management",
    "postharvest",
    "harvest",
]


def number(text):
    """A float, or None when the cell is blank or not a number.

    The schema separates multiple values with '..' (a site spanning a range of
    coordinates, for instance); we take the first one.
    """
    if text is None:
        return None
    try:
        return float(str(text).split("..")[0])
    except ValueError:
        return None


def split_sides(cell):
    """'C: Monoculture_vs_T: Agroforestry' -> ('Monoculture', 'Agroforestry')."""
    if not cell or "_vs_" not in cell:
        return None
    control, treatment = cell.split("_vs_", 1)
    return re.sub(r"^C:\s*", "", control), re.sub(r"^T:\s*", "", treatment)


def contrast(row):
    """The practice, the comparator it was compared against, and the detail.

    Labels are the first term of a '+' joined list; the detail keeps the
    full treatment-side description from the matching *_practice column.
    """
    for theme in THEMES:
        sides = split_sides(row.get(theme + "_theme"))
        if not sides or sides[0] == sides[1]:
            continue
        control, treatment = sides
        detail = split_sides(row.get(theme + "_practice"))
        return {
            "practice": treatment.split(" + ")[0],
            "comparator": control.split(" + ")[0],
            "practiceDetail": detail[1] if detail else treatment,
        }
    return None


def std_dev(row, side):
    """The standard deviation, converting standard errors back with sqrt(n).

    About two thirds of records report no usable dispersion; those give None.
    """
    spread = number(row.get(side + "_out_var_value"))
    n = number(row.get(side + "_out_sample_size"))
    metric = row.get(side + "_out_var_metric") or ""
    if not spread:  # a blank cell, or a reported zero, means no usable dispersion
        return None
    if metric.startswith("SD"):
        return spread
    if metric.startswith(("SE", "SEM")) and n:
        return spread * math.sqrt(n)
    return None  # IQR, confidence intervals and 'Unspecified' are not convertible


def log_ratio_se(c_mean, c_sd, c_n, t_mean, t_sd, t_n):
    """Standard error of ln(T/C), or None when dispersion is missing."""
    if None in (c_sd, t_sd, c_n, t_n) or not c_n or not t_n or not t_mean:
        return None
    return math.sqrt(t_sd**2 / (t_n * t_mean**2) + c_sd**2 / (c_n * c_mean**2))


TRAILING_INITIALS = re.compile(r"\s+(?:[A-Z]\.)+$")


def study_label(authors, year):
    """'Armbrecht I., Perfecto I.' + 2007 -> 'Armbrecht et al. 2007'.

    The two sources spell authors differently, so take the first name listed
    and drop any initials that trail the surname.
    """
    if not authors:
        return str(year or "")
    surname = TRAILING_INITIALS.sub("", authors.split(",")[0].strip())
    return f"{surname} et al. {year}".strip()


def make_record(row, synthesis, serial):
    """One website record, or None if the row cannot be shown on the map."""
    lat, lon = number(row.get("T_site_latitude")), number(row.get("T_site_longitude"))
    c_mean, t_mean = number(row.get("C_out_value")), number(row.get("T_out_value"))
    sides = contrast(row)

    # A record needs a place, a positive control to divide by, and a contrast.
    if lat is None or lon is None or not c_mean or c_mean <= 0 or t_mean is None:
        return None
    if sides is None:
        return None

    c_sd, t_sd = std_dev(row, "C"), std_dev(row, "T")
    c_n, t_n = number(row.get("C_out_sample_size")), number(row.get("T_out_sample_size"))
    ln_rr = math.log(t_mean / c_mean) if t_mean > 0 else None
    crop_full = row.get("T_crop_tree_diversity") or ""
    country = row.get("T_country") or ""

    return {
        "id": f"{synthesis}_{serial}",
        "study_id": row.get("study_id"),
        "synthesis": synthesis,
        "study": study_label(row.get("authors"), row.get("year")),
        "year": int(number(row.get("year")) or 0) or None,
        "doi": row.get("doi") or None,
        "journal": row.get("journal") or None,
        "title": row.get("title") or None,
        "country": country,
        "region": REGIONS.get(country, ""),
        "site": row.get("T_site_id") or None,
        "lat": round(lat, 4),
        "lon": round(lon, 4),
        "crop": crop_full.split("-")[0],
        "cropFull": crop_full,
        "outcome": row.get("out_indicator") or "",
        "subOutcome": row.get("out_subindicator") or None,
        "unit": row.get("T_out_subindicator_unit") or None,
        "practice": sides["practice"],
        "practiceDetail": sides["practiceDetail"],
        "comparator": sides["comparator"],
        "cMean": c_mean,
        "cSD": c_sd,
        "cN": c_n,
        "tMean": t_mean,
        "tSD": t_sd,
        "tN": t_n,
        "lnRR": None if ln_rr is None else round(ln_rr, 4),
        "lnRR_SE": _round(log_ratio_se(c_mean, c_sd, c_n, t_mean, t_sd, t_n), 4),
        "value": round((t_mean - c_mean) / c_mean * 100, 1),
        "years": number(row.get("exp_duration")),
    }


def _round(value, places):
    return None if value is None else round(value, places)


def synthesis_name(path):
    """'fomd10_clean_MD_Jones_21_A glo_Sc.csv' -> 'MD_Jones_21_A glo_Sc'."""
    return os.path.basename(path).replace("fomd10_clean_", "").replace(".csv", "")


def read_source(path):
    """Every record we can build from one source synthesis."""
    synthesis = synthesis_name(path)
    records = []
    with open(path, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            record = make_record(row, synthesis, len(records) + 1)
            if record:
                records.append(record)
    print(f"  {synthesis}: {len(records)} records")
    return records


HEADER = """/* Agroecology Knowledge Hub, website dataset. Generated by build.py, do not edit.
   One record = one control-vs-treatment comparison for one outcome.
   value = percentage change of the treatment mean against the control mean (display only)
   lnRR  = log response ratio, ln(T/C); lnRR_SE is null where no dispersion was reported. */
window.KH_DATA = """

CSV_COLUMNS = [
    "id", "study_id", "synthesis", "study", "year", "doi", "journal", "title",
    "country", "region", "site", "lat", "lon", "crop", "cropFull",
    "outcome", "subOutcome", "unit", "practice", "practiceDetail", "comparator",
    "cMean", "cSD", "cN", "tMean", "tSD", "tN", "lnRR", "lnRR_SE", "value", "years",
]


def write_outputs(records):
    os.makedirs(OUT_DIR, exist_ok=True)

    js_path = os.path.join(OUT_DIR, "data.js")
    with open(js_path, "w", encoding="utf-8") as handle:
        handle.write(HEADER + json.dumps(records, separators=(",", ":")) + ";\n")

    csv_path = os.path.join(OUT_DIR, "data.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows({k: r[k] for k in CSV_COLUMNS} for r in records)

    return js_path, csv_path


def main():
    sources = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.csv")))
    if not sources:
        raise SystemExit(f"No source CSVs found in {SOURCE_DIR}")

    print(f"Reading {len(sources)} source syntheses:")
    records = [r for path in sources for r in read_source(path)]

    js_path, csv_path = write_outputs(records)
    countries = {r["country"] for r in records}
    print(f"\n{len(records)} records, {len(countries)} countries")
    print(f"Wrote {js_path}")
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
