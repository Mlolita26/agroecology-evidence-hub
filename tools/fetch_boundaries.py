"""Fetch the regional boundary files the map draws, and trim them for the web.

The site used to fetch these from geoBoundaries on every country click. That
made the map depend on somebody else's repository staying where it is, and it
broke silently when it moved. Now they live in docs/vendor/adm1/ and this
script is how they get there.

    python tools/fetch_boundaries.py            # every country in the data
    python tools/fetch_boundaries.py BRA NGA    # just these

Run it when a new country appears in the data. build.py tells you when one is
missing. Standard library only, so it keeps working.

Two things shrink the files, neither visible on the map:

  - geoBoundaries ships 15 decimal places, which is sub-nanometre. Four places
    is about 11 metres.
  - The outlines are drawn as hairlines behind the points, so vertices that sit
    within a few hundred metres of the line they span add nothing.

Together that takes about 14 MB down to under 2 MB.
"""

import io
import json
import os
import sys
import urllib.request

WEBSITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# build.py keeps the one country -> ISO3 table. Import it rather than holding a
# second copy here, which would quietly go out of date.
sys.path.insert(0, WEBSITE_DIR)
from build import ISO3  # noqa: E402 - has to follow the line above

OUT_DIR = os.path.join(WEBSITE_DIR, "docs", "vendor", "adm1")
URL = ("https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/main"
       "/releaseData/gbOpen/{0}/ADM1/geoBoundaries-{0}-ADM1_simplified.geojson")

PLACES = 4        # degrees kept, about 11 m
TOLERANCE = 0.003  # degrees, about 330 m: below one pixel at country zoom


def simplify(points, tol):
    """Douglas-Peucker: keep the points that carry the shape, drop the rest.

    Iterative rather than recursive, because a long coastline would otherwise
    run past Python's recursion limit.
    """
    if len(points) < 3:
        return points
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        start, end = stack.pop()
        x1, y1 = points[start]
        x2, y2 = points[end]
        dx, dy = x2 - x1, y2 - y1
        span = dx * dx + dy * dy
        worst, at = 0.0, start
        for i in range(start + 1, end):
            x, y = points[i]
            if span == 0:
                d = (x - x1) ** 2 + (y - y1) ** 2
            else:
                t = ((x - x1) * dx + (y - y1) * dy) / span
                t = 0.0 if t < 0 else 1.0 if t > 1 else t
                d = (x - x1 - t * dx) ** 2 + (y - y1 - t * dy) ** 2
            if d > worst:
                worst, at = d, i
        if worst > tol * tol:
            keep[at] = True
            stack.append((start, at))
            stack.append((at, end))
    return [p for p, k in zip(points, keep) if k]


def trim(ring):
    """Round a ring, drop repeated points, then simplify. None if too small."""
    rounded = []
    for x, y in ring:
        p = [round(x, PLACES), round(y, PLACES)]
        if not rounded or p != rounded[-1]:
            rounded.append(p)
    out = simplify(rounded, TOLERANCE)
    if len(out) >= 4 and out[0] != out[-1]:
        out.append(out[0])          # a ring has to close
    return out if len(out) >= 4 else None


def trim_coords(coords, depth):
    """Rings sit one level deeper in a MultiPolygon than in a Polygon."""
    if depth == 1:
        return trim(coords)
    kept = [trim_coords(c, depth - 1) for c in coords]
    kept = [k for k in kept if k]
    return kept or None


def fetch(iso):
    with urllib.request.urlopen(URL.format(iso)) as r:
        raw = r.read()
    features = []
    for f in json.loads(raw).get("features", []):
        g = f.get("geometry") or {}
        depth = {"Polygon": 2, "MultiPolygon": 3}.get(g.get("type"))
        if not depth:
            continue
        coords = trim_coords(g["coordinates"], depth)
        if not coords:
            continue
        # the map only ever shows the region name, on hover
        features.append({
            "type": "Feature",
            "properties": {"shapeName": (f.get("properties") or {}).get("shapeName")},
            "geometry": {"type": g["type"], "coordinates": coords},
        })

    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, iso + ".json")
    io.open(dest, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"type": "FeatureCollection", "features": features}, separators=(",", ":")))
    return len(raw), os.path.getsize(dest), len(features)


def main():
    wanted = [a.upper() for a in sys.argv[1:]] or sorted(set(ISO3.values()))
    before = after = 0
    for iso in wanted:
        try:
            raw, small, n = fetch(iso)
        except Exception as err:                       # noqa: BLE001 - report and carry on
            print("  %s  FAILED: %s" % (iso, err))
            continue
        before += raw
        after += small
        print("  %s  %6.0f KB -> %5.0f KB  %2d regions" % (iso, raw / 1024, small / 1024, n))
    if before:
        print("\ntotal %.1f MB -> %.1f MB  (%.0f%% smaller)"
              % (before / 1e6, after / 1e6, 100 * (1 - after / before)))


if __name__ == "__main__":
    main()
