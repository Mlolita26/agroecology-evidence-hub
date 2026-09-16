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

## Partner logos are still text

The partner band at the foot of the About page currently sets each partner's
name in type, because no logo files were supplied. To use a real logo, put the
file in `img/logos/` and swap the `<span>` for an `<img>` in `index.html`:

```html
<a class="logo" href="https://www.cirad.fr" target="_blank" rel="noopener">
  <img src="img/logos/cirad.svg" alt="CIRAD">
</a>
```

SVG is best, or PNG at about 200 pixels tall on a transparent background. Logos
are drawn at 38 pixels tall. Most partner logos are dark on transparent and will
disappear in dark mode, so either use a version that works on both, or ask for
one and add a rule in `styles.css`.

The partner links were written from the organisations' usual addresses. Check
each one before the site is promoted.

## Practical notes

- About 1600 by 1100 pixels is plenty. The box is roughly half the page width
  and 320 to 400 pixels tall, and the image is cropped to fill it.
- Keep each file under about 400 KB, or the page gets slow on a phone.
- The caption sits on a solid strip across the bottom, so avoid photographs with
  important detail along the bottom edge.
- Captions are translated. Edit the matching key (`home.06`, `about.04`,
  `methodology.04`) in `../i18n.js` when you change one.
