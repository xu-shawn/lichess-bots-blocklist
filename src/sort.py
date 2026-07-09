#!/usr/bin/env python3
import sys
from collections import Counter

names = Counter()

for file in ("blocklist", "whitelist", "sloplist"):
    with open(file, 'r') as f:
        usernames = sorted(set(f), key=str.lower)
    # newline='\n' stops Windows from writing CRLF; lists must stay LF everywhere.
    with open(file, 'w', newline='\n') as f:
        f.writelines(usernames)
    names.update(username.strip().lower() for username in usernames)

# Lichess usernames are case-insensitive; each should appear once, on one list.
duplicates = sorted(name for name, count in names.items() if count > 1)
if duplicates:
    sys.exit("Duplicate usernames: " + ", ".join(duplicates))