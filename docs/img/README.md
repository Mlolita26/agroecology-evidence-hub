# Hero photographs

Right now every page header shows the dataset itself: one small cell per
comparison, coloured teal for a decrease and pink for an increase. It is a real
picture of the evidence rather than decoration, and it costs nothing to license.

If you would rather show a photograph, put the file in this folder and name it
on the page header in `index.html`:

```html
<figure class="hero-art" data-art="outcome" data-photo="img/about.jpg">
```

The photograph then replaces the artwork on that page. Remove `data-photo` to
get the artwork back. Each page can differ, so you can use a photograph on Home
and keep the artwork elsewhere.

Practical notes:

- About 1600 by 1100 pixels is plenty. The box is roughly half the page width
  and 320 to 400 pixels tall, and the image is cropped to fill it.
- Keep each file under about 400 KB, or the page gets slow on a phone.
- The caption underneath sits on a translucent strip, so avoid photographs with
  important detail along the bottom edge.
- Use photographs the project has the right to publish. The repository is
  public, so anything added here is public too. Credit the photographer in the
  caption.
