#!/usr/bin/env python
"""
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
"""

import json
import glob
import csv

def buildClassList():
    classes = []
    cin = open('ClassList.csv', 'rU')
    cread = csv.reader(cin)
    for course, count in cread:
        if course not in classes:
            classes.append(course)
    return iter(classes)
        
def combineLogs(className, logFiles):
    lineDict = {}
    dc = json.JSONDecoder()
    for fname in logFiles:
        inf = open(fname, 'r')
        lineNo = 1
        for line in inf:
            try:
                dcl = dc.decode(line)
                ts = dcl['time']
                if ts not in lineDict:
                    lineDict[ts] = [line]
                else:
                    lineDict[ts].append(line)
                lineNo += 1
            except ValueError:
                print 'JSON error at line', str(lineNo)
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

if __name__ == '__main__':
    
    classes = buildClassList()
    
    for cl in classes:
        print 'about to process logs for', cl
        prodLogs = []
        logFiles = glob.glob('*/' + cl + '*')
        for f in logFiles:
            print 'processing log', f
            prodLogs.append(f)
        prodDict = combineLogs(cl, prodLogs)
        writeCombLog(cl + '.log', prodDict)



