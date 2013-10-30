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
import glob

classes = ['AI12.1x', 'AI12.2x', 'CB22.1x', 
           'CB22x', 'CS50x', 'CS50', 'ER22x', 
           'GSE1x', 'HKS211.1x','HKS_211', 'HDS1544',
           'HLS1','HMS214x', 'ITCx', 'MCB80.1x', 
           'PH201x', 'PH207x', 'PH278x', 'PH278X',
           'HS221', 'SPU17x', 'SPU27x', 'SPU27X', 'SW12', ]

def combineLogs(className, logFiles):
    lineDict = {}
    dc = json.JSONDecoder()
    for fname in logFiles:
        inf = open(fname, 'r')
        for line in inf:
            dcl = dc.decode(line)
            ts = dcl['time']
            if ts not in lineDict:
                lineDict[ts] = [line]
            else:
                lineDict[ts].append(line)
        inf.close()
    return lineDict

def writeCombLog(fname, log):
    i = 0
    if len(log) < 1:
        print 'Nothing to write for log', fname
        return
    outfile = open(fname, 'w')
    for d in sorted(iter(log)):
        for l in log[d]:
            i += 1
            outfile.write(l)
    print 'wrote', str(i), 'lines to output file', fname
    outfile.close()

for cl in classes:
    edgeLogs = []
    prodLogs = []
    logFiles = glob.glob('*/' + cl + '*')
    for f in logFiles:
        if 'edge' in f:
            edgeLogs.append(f)
        else:
            prodLogs.append(f)
    edgeDict = combineLogs(cl, edgeLogs)
    prodDict = combineLogs(cl, prodLogs)
    writeCombLog(cl + 'edge.log', edgeDict)
    writeCombLog(cl + 'prod.log', prodDict)



