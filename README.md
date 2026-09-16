# Agroecology Evidence Hub, website

**Live site: https://mlolita26.github.io/agroecology-evidence-hub/**

The website shows what happens when farmers use agroecological practices instead
of conventional ones. Every dot on the map is one field comparison from a
published study: a place, a crop, a practice, and how much better or worse the
result was than the plot it was compared against. You can filter by country,
crop, outcome and practice, read the summary that is written from whatever you
picked, and download your selection as a spreadsheet.

Under the hood it is a static site. A Python script turns the harmonised
effect-size tables into one data file, and the browser does the rest. There is
no server and no database.

## Layout

```
build.py     reads the source CSVs and writes docs/data.js and docs/data.csv
docs/        the website itself, and the folder GitHub Pages serves
  index.html   all six pages
  styles.css   design tokens, both themes, masthead, document pages
  explore.css  toolbar, map, summary, heatmap, table, record panel
  app.js       routing, filtering, map, heatmap, table, CSV download
  data.js      generated, not in git, do not edit
  data.csv     generated, not in git, the same table as a raw file
```

**The dataset is not in this repository yet.** `data.js` and `data.csv` are
git-ignored while the review is still a draft, so a fresh clone shows the site
with a "no dataset loaded" banner until you run `build.py`. Once the team
agrees to publish, drop those two lines from `.gitignore` and commit them.

## Rebuilding the data

Run this whenever a new synthesis is harmonised, or an existing one changes:

```
python build.py
```

It reads every CSV in the clean effect-size folder:

```
Agroecology_Evidence_Hub/02.FOMD/04.metadata_effectsize/03.fomd10_clean
```

and prints how many records each source contributed. If your copy of the Hub is
somewhere other than the default OneDrive path, edit `SOURCE_DIR` at the top of
`build.py`. Only the standard library is needed, so there is nothing to install.

Then commit the regenerated files and push; GitHub Pages redeploys on its own.

## Viewing the site locally

```
python -m http.server -d docs 8000
```

and open <http://localhost:8000>. Opening `index.html` straight from the file
system also works, but a local server is closer to the real thing.

## What one record is

One control-versus-treatment comparison, for one outcome, at one place.

- `practice` is the treatment side of the contrast, `comparator` the control
  side. Both stay visible in the interface, because a treatment arm is not
  automatically agroecological; that is sometimes an analytical judgement.
- `value` is the percentage change of the treatment mean against the control
  mean. It is a reading aid only.
- `lnRR` is `ln(T/C)`. `lnRR_SE` is empty for about two thirds of records,
  because the source reported no usable dispersion.
- Rows are dropped when they have no coordinates, no positive control mean, or
  no practice contrast.

Statistics on the site are medians, not means: the distribution has a long tail
and means mislead.

## Scope

The Hub is global. Which countries appear depends on which syntheses have been
harmonised so far, not on any geographic limit. Reporting follows ROSES.

## Publishing

The site is served by GitHub Pages from the `docs/` folder on `main`.
Push to `main` and the change is live in a minute or two.

## Credits

Boundaries from Natural Earth and geoBoundaries. Maps by Leaflet.
Data CC BY 4.0. Draft, not yet citable.
