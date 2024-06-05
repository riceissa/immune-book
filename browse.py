#!/usr/bin/env python3

import sys

import util


front_to_slug_map = {}
# Initialize the set of known slugs with the section names so that the card
# id's don't collide with the section id's.
slugs = set(util.slugify(x) for x in util.sections)
for section in util.sections:
    for note in util.section_map[section]:
        slug = util.slugify(" ".join(note["Front"].split()[:5]))
        if slug in slugs:
            n = 2
            new_slug = slug + f"-{n}"
            while new_slug in slugs:
                n += 1
                new_slug = slug + f"-{n}"
            slug = new_slug
        slugs.add(slug)
        front_to_slug_map[note["Front"]] = slug

with open("docs/browse/index.html", "w") as f:

    f.write(f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <link rel="stylesheet" href="../base.css">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&amp;family=Source+Serif+Pro:ital,wght@0,400;0,700;1,400;1,700&amp;display=swap" rel="stylesheet">

    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%221em%22 font-size=%2280%22>&#x1F9A0;</text></svg>">

    <title>Browse cards - Immune Book Flashcards</title>
  </head>
  <body>
    <span id="top"></span>
    {util.navbar(1)}
    <main>\n""")

    f.write('<p style="font-size: 80%;">Skip to chapter: ')
    f.write("&nbsp;&middot; ".join(f'<a href="#{util.slugify(section)}">{section}</a>' for section in util.sections))
    f.write("</p>\n")

    for section in util.sections:
        anchor_link = f'<a href="#{util.slugify(section)}" title="Link to this section" class="heading-marker">#</a>'
        toc_link = '<a href="#top" title="Go back to the top of the page" class="heading-marker">&#8617;</a>'
        f.write(f'<h2 id="{util.slugify(section)}">{section} {anchor_link} {toc_link}</h2>\n')
        if not util.section_map[section]:
            f.write("<p>There are no cards for this chapter.</p>\n")
        for note in util.section_map[section]:
            note_div_id = front_to_slug_map[note["Front"]]
            f.write(f'<div id="{note_div_id}" class="card">\n')

            f.write('<div class="front">\n')
            f.write(note["Front"] + "\n")
            f.write("</div>\n")

            f.write("<hr>\n")

            f.write('<div class="back">\n')
            f.write(note["Back"] + "\n")
            f.write("</div>\n")

            f.write('<div class="notes">\n')
            f.write(note["Notes"] + "\n")
            f.write("</div>\n")

            f.write("</div>\n")

    f.write("""
    </main>
  </body>
</html>\n""")
