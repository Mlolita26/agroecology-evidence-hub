"""Build the website dataset from the harmonised 10_ schema effect-size tables.

Reads every CSV in the clean effect-size folder, turns each control-vs-treatment
comparison into one website record, and writes docs/data.js.

    python build.py             # build, and stamp the asset links in index.html
    python build.py --dry-run   # read and report, write nothing

Set SOURCE_DIR below if your copy of the Hub lives somewhere else.
"""

import csv
import glob
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter

# The folder on disk is named "Knowledge Hub"; that is the real OneDrive path
# and has nothing to do with what the website calls itself. Do not rename it.
SOURCE_DIR = os.path.expanduser(
    "~/OneDrive - CGIAR/Alliance-Agroecology Knowledge Hub - General"
    "/Agroecology_Evidence_Hub/02.FOMD/04.metadata_effectsize/03.fomd10_clean"
)
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
ADM1_DIR = os.path.join(OUT_DIR, "vendor", "adm1")

# The whole dataset goes to the browser as one JavaScript file. The server
# compresses it in transit, so the download is not the issue; parsing it and
# holding it in memory is, and so is drawing a point per record. Past this the
# data needs a different shape, not a bigger file. See knowledge/website.md.
MAX_DATA_MB = 20

# Syntheses the website does not publish yet, and why. Everything in the source
# folder is published unless it is named here, so leaving a synthesis out is a
# decision somebody wrote down rather than something that happened quietly.
# Delete an entry to publish it; build.py will tell you if it no longer fits.
SKIP_SOURCES = {
    "MD_Rosen_24_Effec_Sc":
        "ERA, 87,796 records. Two separate reasons. At 65 MB it is past the "
        "limit above, and the map would need the canvas renderer to stay "
        "usable at that many points. And the effect sizes come from a script "
        "with an open bug: see "
        "knowledge/_meta/log/2026-09-28-02-lnrr-cv-imputation-bug.md. "
        "Measured costs: knowledge/_status/website.md.",
}

# The source has no region column. These are the UN M49 sub-regions, which is
# why Malawi, Zambia and Zimbabwe sit in Eastern Africa: that is where the UN
# puts them. Every country in ISO3 below has an entry, so a new country in the
# data is never left without a region to filter on.
REGIONS = {
    "Bangladesh": "Southern Asia", "Benin": "Western Africa", "Bolivia": "South America",
    "Brazil": "South America", "Burkina Faso": "Western Africa", "Cameroon": "Middle Africa",
    "China": "Eastern Asia", "Colombia": "South America", "Ethiopia": "Eastern Africa",
    "Ghana": "Western Africa", "Guatemala": "Central America", "India": "Southern Asia",
    "Indonesia": "South-eastern Asia", "Kenya": "Eastern Africa", "Malawi": "Eastern Africa",
    "Mali": "Western Africa", "Mexico": "Central America", "Morocco": "Northern Africa",
    "Mozambique": "Eastern Africa", "Nepal": "Southern Asia", "Niger": "Western Africa",
    "Nigeria": "Western Africa", "Pakistan": "Southern Asia", "Peru": "South America",
    "Philippines": "South-eastern Asia", "Rwanda": "Eastern Africa", "Senegal": "Western Africa",
    "South Africa": "Southern Africa", "Tanzania": "Eastern Africa", "Tunisia": "Northern Africa",
    "Uganda": "Eastern Africa", "Vietnam": "South-eastern Asia", "Zambia": "Eastern Africa",
    "Zimbabwe": "Eastern Africa",
}

# Terms that mark the conventional side of a comparison. The website always shows
# the agroecological arm as the practice, so when the source put one of these on
# its treatment side the two arms are swapped before anything is computed. When
# both arms carry one (no fertiliser against mineral fertiliser, say) neither is
# agroecological and the row is set aside rather than published.
#
# The list follows knowledge/control_treatment_scoring.md, Gliessman level 0,
# including its rule that the mere absence of an input is not agroecology. That
# document is a draft for Andrea to ratify; the build prints every swap and
# every row set aside so the list can be checked against the data.
COMPARATOR_TERMS = frozenset([
    # diversification
    "Monoculture",
    # tillage
    "Conventional Tillage",
    # nutrients: synthetic inputs, and no inputs at all
    "Inorganic Fertilizer", "External input dependency", "No Fertilizers Applied",
    # pests
    "Synthetic pesticide",
    # biomass
    "Plastic mulch", "No mulch",
    # water: irrigation on its own is not a practice choice on the gradient
    "Irrigation", "Full irrigation", "No irrigation",
    # other absences
    "Unimproved variety", "No Inoculation", "No liming",
])
# Left out on purpose: "Natural Fallow" (a rest period, the temporal arm in
# Jones), "Timber plantation" (the comparator of Paut's agroforestry pairs),
# "No Chemical Applied" (its pairs carry Inoculants on the same side).

# Country -> ISO3, for the regional boundary files in docs/vendor/adm1/.
# This is the only copy: tools/fetch_boundaries.py imports it to know what to
# download, and write_iso3() below hands it to the browser as docs/iso3.js.
ISO3 = {
    "Colombia": "COL", "Ethiopia": "ETH", "Guatemala": "GTM", "India": "IND",
    "Kenya": "KEN", "Malawi": "MWI", "Mexico": "MEX", "Peru": "PER",
    "South Africa": "ZAF", "Tunisia": "TUN", "Vietnam": "VNM", "Zambia": "ZMB",
    "Bangladesh": "BGD", "Benin": "BEN", "Bolivia": "BOL", "Brazil": "BRA",
    "Burkina Faso": "BFA", "Cameroon": "CMR", "China": "CHN", "Ghana": "GHA",
    "Indonesia": "IDN", "Mali": "MLI", "Morocco": "MAR", "Mozambique": "MOZ",
    "Nepal": "NPL", "Niger": "NER", "Nigeria": "NGA", "Pakistan": "PAK",
    "Philippines": "PHL", "Rwanda": "RWA", "Senegal": "SEN", "Tanzania": "TZA",
    "Uganda": "UGA", "Zimbabwe": "ZWE",
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


def first(text):
    """The first value of a '..' separated cell, stripped.

    A row that covers several sites lists one country per site, joined the same
    way the coordinates are. We plot the first coordinate, so we take the first
    country with it; otherwise the cell reads 'Malawi..Malawi..Malawi'.
    """
    if not text:
        return ""
    return str(text).split("..")[0].strip()


def clean(text):
    """A cell as text, with the schema's two ways of saying 'nothing' removed."""
    text = (text or "").strip()
    return "" if text in ("NA", "Unspecified") else text


def split_sides(cell):
    """'C: Monoculture_vs_T: Agroforestry' -> ('Monoculture', 'Agroforestry')."""
    if not cell or "_vs_" not in cell:
        return None
    control, treatment = cell.split("_vs_", 1)
    return re.sub(r"^C:\s*", "", control), re.sub(r"^T:\s*", "", treatment)


def terms(label):
    """'Intercropping + Mulching' -> {'Intercropping', 'Mulching'}."""
    return {t.strip() for t in label.split(" + ") if t.strip()}


def contrast(row):
    """The two arms of the comparison, as the source labelled them.

    Works through THEMES and takes the first one whose two sides differ. Each
    arm gets a label (the first term of a '+' joined list), the full detail
    from the matching *_practice column, and the set of every term seen on
    that side in either column, which is what orient() reads.
    """
    for theme in THEMES:
        sides = split_sides(row.get(theme + "_theme"))
        if not sides or sides[0] == sides[1]:
            continue
        control, treatment = sides
        detail = split_sides(row.get(theme + "_practice")) or (control, treatment)
        return {
            "C": {"label": control.split(" + ")[0], "detail": detail[0],
                  "terms": terms(control) | terms(detail[0])},
            "T": {"label": treatment.split(" + ")[0], "detail": detail[1],
                  "terms": terms(treatment) | terms(detail[1])},
        }
    return None


def orient(sides):
    """Which way round to publish the arms: 'keep', 'swap' or 'lateral'.

    The practice is always the agroecological arm. If only the source's
    treatment carries a conventional term, the arms are the wrong way round
    for us and are swapped. If both do, neither arm is agroecological: the
    comparison is lateral, set aside and not published.
    """
    c_conv = bool(sides["C"]["terms"] & COMPARATOR_TERMS)
    t_conv = bool(sides["T"]["terms"] & COMPARATOR_TERMS)
    if t_conv and c_conv:
        return "lateral"
    if t_conv:
        return "swap"
    return "keep"


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
    """One website record and how it was oriented, or why there is none.

    Returns (status, record). The status is 'kept' or 'swapped' when there is
    a record, and 'no contrast', 'incomplete' or 'lateral' when there is not.
    """
    sides = contrast(row)
    if sides is None:
        return "no contrast", None
    decision = orient(sides)

    # Read the arms through these prefixes, so a swapped comparison is computed
    # the right way round from the start instead of being corrected afterwards.
    c, t = ("T", "C") if decision == "swap" else ("C", "T")
    arm = lambda side, column: row.get(side + column)  # noqa: E731
    either = lambda column: clean(arm(t, column)) or clean(arm(c, column))  # noqa: E731

    lat, lon = number(either("_site_latitude")), number(either("_site_longitude"))
    c_mean, t_mean = number(arm(c, "_out_value")), number(arm(t, "_out_value"))
    # A record needs a place, a positive control to divide by, and a treatment.
    if lat is None or lon is None or not c_mean or c_mean <= 0 or t_mean is None:
        return "incomplete", None
    if decision == "lateral":
        return "lateral", None

    c_sd, t_sd = std_dev(row, c), std_dev(row, t)
    c_n, t_n = number(arm(c, "_out_sample_size")), number(arm(t, "_out_sample_size"))
    ln_rr = math.log(t_mean / c_mean) if t_mean > 0 else None
    crop_full = either("_crop_tree_diversity")
    country = first(either("_country"))
    practice, comparator = (sides["C"], sides["T"]) if decision == "swap" else (sides["T"], sides["C"])
    status = "swapped" if decision == "swap" else "kept"

    return status, {
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
        "site": either("_site_id") or None,
        "lat": round(lat, 4),
        "lon": round(lon, 4),
        "crop": crop_full.split("-")[0],
        "cropFull": crop_full,
        "pillar": clean(row.get("out_pillar")),
        "subPillar": clean(row.get("out_subpillar")),
        "outcome": clean(row.get("out_indicator")),
        "subOutcome": clean(row.get("out_subindicator")) or None,
        "group": clean(first(row.get("bio_func_group"))),
        "unit": either("_out_subindicator_unit") or None,
        "practice": practice["label"],
        "practiceDetail": practice["detail"],
        "comparator": comparator["label"],
        "comparatorDetail": comparator["detail"],
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
        "swapped": decision == "swap",
    }


def _round(value, places):
    return None if value is None else round(value, places)


def synthesis_name(path):
    """'fomd10_clean_MD_Jones_21_A glo_Sc.csv' -> 'MD_Jones_21_A glo_Sc'."""
    return os.path.basename(path).replace("fomd10_clean_", "").replace(".csv", "")


def read_source(path):
    """Every record we can build from one source synthesis.

    Prints what happened to the rows as it goes: how many were swapped and
    how many set aside, and which pairs of arms those were, so the
    COMPARATOR_TERMS list can be checked against the data every time.
    """
    synthesis = synthesis_name(path)
    records, tally = [], Counter()
    pairs = {"swapped": Counter(), "lateral": Counter()}
    with open(path, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            status, record = make_record(row, synthesis, len(records) + 1)
            tally[status] += 1
            if record:
                records.append(record)
            if status in pairs:
                sides = contrast(row)
                pairs[status][(sides["C"]["label"], sides["T"]["label"])] += 1

    print(f"  {synthesis}: {len(records)} records "
          f"({tally['kept']} as the source had them, {tally['swapped']} swapped); "
          f"{tally['lateral']} set aside as lateral; "
          f"{tally['incomplete'] + tally['no contrast']} unusable")
    for status, note in (("swapped", "swapped"), ("lateral", "set aside")):
        for (control, treatment), n in pairs[status].most_common():
            print(f"      {n:4d} {note}: source control '{control}' vs treatment '{treatment}'")
    return records


HEADER = """/* Agroecology Evidence Hub, website dataset. Generated by build.py, do not edit.
   One record = one comparison between an agroecological practice (T) and a less
   agroecological alternative (C), for one outcome. practice is always the
   agroecological arm; swapped is true where the source had the arms the other
   way round and build.py turned them.
   lnRR  = log response ratio, ln(T/C); lnRR_SE is null where no dispersion was reported.
   value = percentage change of T against C, kept for the download only. */
window.KH_DATA = """

CSV_COLUMNS = [
    "id", "study_id", "synthesis", "study", "year", "doi", "journal", "title",
    "country", "region", "site", "lat", "lon", "crop", "cropFull",
    "pillar", "subPillar", "outcome", "subOutcome", "group", "unit",
    "practice", "practiceDetail", "comparator", "comparatorDetail",
    "cMean", "cSD", "cN", "tMean", "tSD", "tN", "lnRR", "lnRR_SE", "value", "years",
    "swapped",
]


def write_outputs(records):
    """Write docs/data.js and docs/data.csv, or (None, None) if they are too big.

    Refusing leaves the last dataset that fit in place, so the site keeps
    working while somebody deals with the size.
    """
    os.makedirs(OUT_DIR, exist_ok=True)
    body = (HEADER + json.dumps(records, separators=(",", ":")) + ";\n"
            "/* column order of the download, the same as data.csv */\n"
            "window.KH_COLUMNS = " + json.dumps(CSV_COLUMNS) + ";\n")

    megabytes = len(body.encode("utf-8")) / 1e6
    if megabytes > MAX_DATA_MB:
        print(f"\nSTOPPED. data.js would be {megabytes:.0f} MB, over the "
              f"{MAX_DATA_MB} MB limit, so nothing was written.")
        print(f"  {len(records)} records is more than one file should carry. The "
              "server compresses")
        print("  it, so the download is smaller than this, but every visitor still "
              "parses all")
        print("  of it and holds it in memory before the map draws.")
        print("  The site still has the last dataset that fit.")
        return None, None

    js_path = os.path.join(OUT_DIR, "data.js")
    with open(js_path, "w", encoding="utf-8") as handle:
        handle.write(body)

    csv_path = os.path.join(OUT_DIR, "data.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows({k: r[k] for k in CSV_COLUMNS} for r in records)

    return js_path, csv_path


def write_iso3():
    """Write the country -> ISO3 table the browser needs, as docs/iso3.js.

    app.js uses it to pick the right file out of vendor/adm1/. Generating it
    from the table above means there is one list, not two that drift apart.
    """
    path = os.path.join(OUT_DIR, "iso3.js")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("/* Country -> ISO3, for the boundary files in vendor/adm1/.\n"
                     "   Generated by build.py, do not edit. */\n"
                     "window.KH_ISO3 = "
                     + json.dumps(ISO3, indent=2, sort_keys=True) + ";\n")
    return path


def check_boundaries(records):
    """Say which countries the map cannot outline, so it is never a surprise.

    A country needs a code in ISO3 above and a file in docs/vendor/adm1/.
    Both gaps print the command that fixes them.
    """
    countries = sorted({r["country"] for r in records if r["country"]})
    have = {n[:-5] for n in os.listdir(ADM1_DIR)} if os.path.isdir(ADM1_DIR) else set()
    unknown = [c for c in countries if c not in ISO3]
    missing = sorted({ISO3[c] for c in countries if c in ISO3 and ISO3[c] not in have})

    if unknown:
        print(f"\n{len(unknown)} countries in the data have no ISO3 code in build.py:")
        print("  " + ", ".join(unknown))
    if missing:
        print(f"\n{len(missing)} boundary files are missing. To fetch them:")
        print("  python tools/fetch_boundaries.py " + " ".join(missing))
    if not unknown and not missing:
        print(f"\nAll {len(countries)} countries in the data have a boundary file.")



# Files index.html links to. Each gets a tag built from its own contents.
ASSETS = ["styles.css", "explore.css", "data.js", "iso3.js", "i18n.js", "vocab.js",
          "app.js"]


def stamp_assets():
    """Tag each asset link in index.html with a hash of that file's contents.

    Browsers cache by URL. An unchanged file keeps its tag and stays cached;
    a changed file gets a new tag and is fetched again straight away. Doing it
    from the contents means nobody has to remember to bump a version number.
    """
    page = os.path.join(OUT_DIR, "index.html")
    html = open(page, encoding="utf-8").read()
    for name in ASSETS:
        path = os.path.join(OUT_DIR, name)
        if not os.path.exists(path):
            continue
        tag = hashlib.md5(open(path, "rb").read()).hexdigest()[:8]
        html = re.sub(r'"' + re.escape(name) + r'(\?v=[0-9a-f]+)?"', f'"{name}?v={tag}"', html)
    open(page, "w", encoding="utf-8", newline="\n").write(html)
    print(f"Stamped {len(ASSETS)} asset links in {page}")


def main():
    dry_run = "--dry-run" in sys.argv[1:]
    sources = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.csv")))
    if not sources:
        raise SystemExit(f"No source CSVs found in {SOURCE_DIR}")

    skipped = [p for p in sources if synthesis_name(p) in SKIP_SOURCES]
    sources = [p for p in sources if synthesis_name(p) not in SKIP_SOURCES]

    print(f"Reading {len(sources)} source syntheses:")
    records = [r for path in sources for r in read_source(path)]

    for path in skipped:
        name = synthesis_name(path)
        print(f"\nNot published: {name}")
        print("  " + SKIP_SOURCES[name])
    countries = {r["country"] for r in records}
    print(f"\n{len(records)} records, {len(countries)} countries")

    no_region = sorted(c for c in countries if c not in REGIONS)
    if no_region:
        print(f"\n{len(no_region)} countries have no entry in REGIONS, so the region "
              "filter cannot reach them:")
        print("  " + ", ".join(no_region))
    check_boundaries(records)

    if dry_run:
        print("\nDry run: nothing written.")
        return

    js_path, csv_path = write_outputs(records)
    if js_path:
        print(f"Wrote {js_path}")
        print(f"Wrote {csv_path}")
    print(f"Wrote {write_iso3()}")
    stamp_assets()
    if not js_path:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
