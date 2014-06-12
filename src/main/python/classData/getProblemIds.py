#!/usr/bin/env python
"""

"""
import csv
import sys

inf = csv.reader(open(sys.argv[1], 'r'))
idDict = {}

for row in inf:
    if (row[1] == 'problem'):
        modId = row[2]
        modId = modId[modId.rfind('/')+1:]
        if modId not in idDict:
            idDict[modId] = 1
        else:
            idDict[modId] += 1

outf = csv.writer(open('pidCounts.csv', 'w'))
outf.writerow(['UUID', 'count'])

for pId in iter(idDict):
    outf.writerow([pId, idDict[pId]])
    
    
