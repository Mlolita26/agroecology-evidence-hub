# Hero photographs

Three pages use a photograph in the header:

| Page | File | Caption credit |
|---|---|---|
| Home | `home.jpg` | Olivier Asselin / FAO |
| About | `about.webp` | not known |
| Methodology | `methodology.jpg` | not known |

**Rights are not confirmed.** These came from the team's own downloads and only
the FAO photograph has a known photographer. This repository is public, so
before the site is promoted, check that the project may publish each one and put
the right credit in its caption. If a photograph cannot be cleared, delete the
file and remove `data-photo` from that page; the fallback artwork returns on its
own.

## Get involved and Contact still need a photograph

Both currently fall back to the artwork, which draws the dataset itself. To give
them a photograph, drop the file here and name it on that page's header in
`index.html`:

```html
<figure class="hero-art" data-photo="img/involved.jpg">
```

Remove `data-photo` to go back to the artwork. Each page is independent.

## Practical notes

- About 1600 by 1100 pixels is plenty. The box is roughly half the page width
  and 320 to 400 pixels tall, and the image is cropped to fill it.
- Keep each file under about 400 KB, or the page gets slow on a phone.
- The caption sits on a solid strip across the bottom, so avoid photographs with
  important detail along the bottom edge.
- Captions are translated. Edit the matching key (`home.06`, `about.04`,
  `methodology.04`) in `../i18n.js` when you change one.
