#!/usr/bin/env python
'''
Combine all of the log files in a particular directory into a single log file


'''

import json
import os

lineDict = {}
dc = json.JSONDecoder()

dirName = os.getcwd()
className = dirName[dirName.rindex('/')+1:]
logList = os.listdir(dirName)
outfile = open(className + 'FullLog', 'w')

for fname in logList:
    inf = open(fname, 'r')
    for line in inf:
        dcl = dc.decode(line)
        ts = dcl['time']
        if ts not in lineDict:
            lineDict[ts] = [line]
        else:
            lineDict[ts].append(line)
    inf.close()

i = 0
for d in sorted(iter(lineDict)):
    for l in lineDict[d]:
        i += 1
        outfile.write(l)

print 'wrote ' + str(i) + ' lines to output file'
outfile.close()
