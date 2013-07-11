#!/usr/bin/env python
'''
Combine all of the log files in a directory into a single log file

This script assumes that all of the log files to be combined are in a 
single directory, and that the name of the directory is the name of the 
class. The program will combine all of the files into a single file, with
the lines in timestamp order. While unlikely, it is possible that multiple
lines have the same timestamp; if that happens they will be ordered in the
order they are seen when read.

The main use for this script is to combine all of the files for a given
week (as obtained from edX) into a file for that week. However, if multiple
weeks log files are in the directory, they will all be combined. 
'''

import json
import os

lineDict = {}
dc = json.JSONDecoder()

dirname = os.getcwd()
classname = dirname[dirname.rindex('/')+1:]
logList = os.listdir(dirname)

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

outfile = open(classname + 'WeekLog', 'w')
i = 0
for d in sorted(iter(lineDict)):
    for l in lineDict[d]:
        i += 1
        outfile.write(l)
        
print 'wrote ' + str(i) + ' lines to output file'
outfile.close()
