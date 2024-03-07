#!/usr/bin/env python3

import subprocess
import sys
import pathlib
import re
from anki.collection import Collection

import util

def html_to_markdown(html_string):
    try:
        # markdown_strict is needed here so that things like double quotes
        # aren't unnecessarily backslash-escaped. wrap=none is for Orbit;
        # Orbit will faithfully translate newlines appearing in the source
        # so we need to remove superfluous newlines created by pandoc's
        # markdown output.
        p = subprocess.run(["pandoc", "-f", "html", "-t", "markdown_strict", "--wrap=none"],
                           input=html_string.encode('utf-8'), check=True,
                           capture_output=True)
        return p.stdout.decode('utf-8').replace('"', "&quot;").strip()
    except subprocess.CalledProcessError as e:
        print("Error running pandoc:",
              "error code:", e.returncode,
              "error message:", e.stderr.decode("utf-8"), file=sys.stderr)
        sys.exit()


with open("docs/orbit/index.html", "w") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
      <link rel="stylesheet" href="../base.css">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&amp;family=Source+Serif+Pro:ital,wght@0,400;0,700;1,400;1,700&amp;display=swap" rel="stylesheet">

    <title>Orbit index - GEB Typogenetics/DNA/RNA Flashcards</title>

    </head>
    <body>
    {util.navbar(1)}
    <main>

    <h2>Orbit index</h2>

    <p>Pick a section below to collect its cards:</p>
    """)

    f.write("<ul>")

    for section in util.sections:
        if not util.section_map[section]:
            f.write(f"<li>{section} (no cards for this section)</li>\n")
        else:
            num_cards = len(util.section_map[section])
            f.write(f'<li><a href="{util.slugify(section)}">{section}</a> ({num_cards} card{"" if num_cards == 1 else "s"})</li>\n')

            section_dir = f"docs/orbit/{util.slugify(section)}/"
            pathlib.Path(section_dir).mkdir(exist_ok=True)
            with open(section_dir + "index.html", "w") as g:
                g.write(f"""<!DOCTYPE html>
            <html lang="en">
                <head>
                  <meta charset="utf-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
                  <title>{section} - GEB Typogenetics/DNA/RNA Flashcards</title>
                  <link rel="canonical" href="https://riceissa.github.io/geb-typogenetics-dna-rna/orbit/{util.slugify(section)}/">
                  <meta property="og:title" content="{section}">
                  <meta property="og:site_name" content="GEB Typogenetics/DNA/RNA flashcards">
                  <link rel="stylesheet" href="../../base.css">

                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
                    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&amp;family=Source+Serif+Pro:ital,wght@0,400;0,700;1,400;1,700&amp;display=swap" rel="stylesheet">

                  <script type="module" src="https://js.withorbit.com/orbit-web-component.js"></script>
                </head>
                <body>
                    {util.navbar(2, optional=[("Back to Orbit index", "../")])}
                <main>
                      <h2>{section}</h2>
                      <orbit-reviewarea color="yellow">
                """)

                for note in util.section_map[section]:
                    note_front = html_to_markdown(note["Front"])
                    note_back = html_to_markdown(note["Back"])
                    note_notes = html_to_markdown(note["Notes"])
                    question_attachments = ""
                    answer_attachments = ""
                    img_regex = r'!\[\]\(([^) ]+)\)'
                    match = re.findall(img_regex, note_front)
                    if len(match) > 1:
                        raise ValueError("Question cannot contain more than one image!")
                    if len(match) == 1:
                        image_url = "https://riceissa.github.io/geb-typogenetics-dna-rna/browse/" + match[0]
                        question_attachments = f'question-attachments="{image_url}"'
                        note_front = re.sub(img_regex, "", note_front).strip()
                    match = re.findall(img_regex, note_back)
                    if len(match) > 1:
                        raise ValueError("Answer cannot contain more than one image!")
                    if match:
                        image_url = "https://riceissa.github.io/geb-typogenetics-dna-rna/browse/" + match[0]
                        answer_attachments = f'answer-attachments="{image_url}"'
                        note_back = re.sub(img_regex, "", note_back).strip()
                    g.write(f"""<orbit-prompt
                            question="{note_front}"
                            {question_attachments}
                            {answer_attachments}
                          answer="{note_back}

{note_notes}"
                        ></orbit-prompt>
                      """)


                g.write("""
                      </orbit-reviewarea>
                        </main>
                        </body>
                        </html>
                """)

    f.write("</ul>")


    f.write("""
            </main>
            </body>
            </html>
    """)

