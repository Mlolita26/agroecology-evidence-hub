# Other people's code and data, kept here on purpose

Everything the website needs is in this folder. The pages load nothing from
anyone else's server: no CDN, no Google Fonts, no live map data. Open the site
with the network switched off after the first visit and it still works.

That is deliberate. A site that fetches a script from somewhere else only works
for as long as that somewhere else keeps serving it, at the same address, with
the same contents. Over a few years that is not a safe bet. It also means every
visitor is announced to those servers, which is not something we can promise
people we control.

Nothing in here is ours, and nothing in here should be edited. To change a
version, fetch the new one and replace the file whole.

## What is here

| File | What it is | Version | Where it came from |
| --- | --- | --- | --- |
| `leaflet.js`, `leaflet.css`, `images/` | the map | 1.9.4 | unpkg.com/leaflet@1.9.4/dist/ |
| `topojson-client.min.js` | unpacks the country shapes | 3.1.0 | unpkg.com/topojson-client@3 |
| `countries-110m.json` | world country outlines | world-atlas 2.0.2 | unpkg.com/world-atlas@2/countries-110m.json |
| `fonts.css`, `fonts/` | Instrument Serif, Archivo, Spline Sans Mono | — | fonts.googleapis.com, then the woff2 files |
| `adm1/` | regions inside each country | geoBoundaries gbOpen | see below |

The five PNGs in `images/` belong to Leaflet and are named in `leaflet.css`.
They are the layer-switcher and marker icons. Keep them next to it.

`fonts.css` is the stylesheet Google returns, with every `fonts.gstatic.com`
address swapped for the matching file in `fonts/`. If you add a weight or a
style, refetch the `css2` URL written at the top of that file and redo the swap.

## The country region files in `adm1/`

One file per country, named by ISO3 code, drawn when somebody clicks a country
on the explore map. These used to be fetched from geoBoundaries on every click,
which made the map depend on their repository staying where it was, and it broke
without saying so when a file moved.

They are produced by `tools/fetch_boundaries.py`, which downloads the ADM1 set
and trims it for the web: coordinates rounded to four decimal places, about
11 metres, and vertices dropped where they sit within roughly 330 metres of the
line they span. At the zoom these are drawn, both are well under a pixel. That
takes 14.7 MB down to 2.8 MB with no visible difference.

To add a country:

    python tools/fetch_boundaries.py BRA

`build.py` prints the exact command when the data contains a country with no
file, so you do not have to remember which ones are missing.

## Licences

These are other people's work, under their own terms.

- Leaflet, topojson-client, world-atlas: BSD 2-Clause / ISC. Free to
  redistribute, which is what keeping a copy here does.
- Instrument Serif, Archivo, Spline Sans Mono: SIL Open Font License 1.1.
  Free to bundle and serve.
- geoBoundaries gbOpen: CC BY 4.0. Credited on the about page. If you add
  countries, the credit still covers them.

Nothing here is copyleft and nothing needs a notice on the page beyond the
geoBoundaries credit already there.
