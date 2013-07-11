#!/usr/bin/env python

import json
import sys

f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'w')
dc = json.JSONDecoder()

for line in f1:
    dcl = dc.decode(line)
    f2.write(dcl['username'] + '\n')
