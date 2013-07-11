#!/usr/bin/env python

import json
import csv
import sys

inFile = open(sys.argv[1], 'r')
outfile = csv.writer(open(sys.argv[2], 'w'))
ipDict = {}

for line in inFile:
    elems = json.loads(line)
    ipAddr = elems['ip']
    if ipAddr in ipDict:
        ipDict[ipAddr] += 1
    else:
        ipDict[ipAddr] = 1

for ipA in sorted(iter(ipDict)):
    outfile.writerow([ipA, ipDict[ipA]])
