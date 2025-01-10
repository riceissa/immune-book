# immune-book

## Installation/generation

This section is only relevant if you want to compile the website locally for development purposes.
If you just want to use the Immune deck, go to <https://riceissa.github.io/immune-book/>.

You will need the command-line programs `unzip` and `pandoc` in order to run the following commands.
If you don't have them, on Ubuntu you can just run `sudo apt install unzip pandoc`.
Also, you will need to install the `anki` Python Pip package. To do this,
you can run `python3 -m pip install -U anki`.

Note also that for now, the scripts (in particular, `media.py`) only work if
the Anki deck was exported using the "Support older Anki versions
(slower/larger files)" option.  This is only a concern if you are editing the
Anki deck and re-exporting it; if you are just using the Anki deck stored at
`docs/immune.apkg` then that deck has already been exported using this option,
so you don't need to do anything.

First download the `.apkg` file into the `docs/` directory, and name it `immune.apkg`. Then run the following commands:

```bash
# .apkg file is actually secretly a zip file. so unzip its contents to a directory called apkg/
unzip -d apkg/ docs/immune.apkg

# Remove unneeded files
rm apkg/meta
rm apkg/collection.anki2

# Rename images/other media files to their correct locations
./media.py

# Generate the browse page
./browse.py

# Generate the Orbit pages
./orbit.py
```
