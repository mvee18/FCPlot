#!/usr/bin/python

import re
import sys

file = sys.argv[1]
# pattern = sys.argv[1]

f = open(file, "r")

for lines in f.readlines():
    str(lines)
    match = re.search('-\d{2}\.\d+', lines)
#   match = re.search(pattern, lines)
    if match:
        print(match.group(0))
