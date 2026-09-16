# Hero photographs

Every page header now uses a photograph.

| Page | File | Source | Credit |
|---|---|---|---|
| Home | `home.jpg` | FAO | Olivier Asselin / FAO |
| About | `about.webp` | not known | **missing** |
| Methodology | `methodology.jpg` | not known | **missing** |
| Get involved | `involved.jpg` | filename suggests IBP, Bolgatanga, March 2022 | **missing** |
| Contact | `contact.jpg` | not known | **missing** |

## Credits are still missing

Only the FAO image has a known photographer. The footer says "Olivier Asselin /
FAO; other credits to follow", which is honest but temporary. Fill in the rest
and update `footer.06` in `../i18n.js` in all three languages. Check too that
the project may publish each one: this repository is public.

If a photograph cannot be cleared, delete the file and remove `data-photo` from
that page in `index.html`. The generated artwork comes back on its own, so the
page never breaks.

## Swapping a photograph

Put the file here and name it on that page's header in `index.html`:

```html
<figure class="hero-art" data-photo="img/involved.jpg">
```

Remove `data-photo` to go back to the artwork. Each page is independent.

- About 1600 by 1100 pixels is plenty. The box is roughly half the page width
  and 320 to 400 pixels tall, and the image is cropped to fill it.
- Keep each file under about 400 KB, or the page gets slow on a phone.

## Partner logos are still text

The partner band at the foot of the About page sets each partner's name in type,
because no logo files were supplied. To use a real logo, put the file in
`img/logos/` and swap the `<span>` for an `<img>`:

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
