#!/usr/bin/env python3

import json
import os

with open("apkg/media", "r") as f:
    j = json.load(f)

    for n in j:
        from_filename = f"apkg/{n}"
        to_filename = f"docs/browse/{j[n]}"
        os.rename(from_filename, to_filename)
        print(f"Moved {from_filename} -> {to_filename}")
