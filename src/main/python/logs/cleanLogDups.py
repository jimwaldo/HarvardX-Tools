#!/usr/bin/env python
"""
Reads an edX supplied log file, finding and eliminating any duplicate lines

Reads an edX log file, finding any duplicate lines. Writes a file with the same
name as the log file with the additional postfix "scrub" that contains only the 
non-duplicated lines. 

At the end of the run, prints out the number of lines read, the number of duplicate
lines, and the number of non-duplicate lines.

This file is left over from the early days of the log file distribution, when logs
for the same day were increasing in size on each release. This hasn't been used for
some time since the size change was repaired.
"""
import json
import sys

class Line(object):
    def __init__(self, lineNo, lineCont):
        self.line = lineNo
        self.content = lineCont


if __name__ == '__main__':
    linedict = {}
    f1 = open(sys.argv[1], 'r')
    f2 = open(sys.argv[1] + 'scrub', 'w')
    ln = 0
    duplines = 0
    dc = json.JSONDecoder()
    for line in f1:
        ln += 1
        dl = dc.decode(line)
        key = dl['time'] + dl['username']
        if key not in linedict:
            f2.write(line)
            lo = Line(ln, line)
            linedict[key] = lo
        elif linedict[key].content == line:
            duplines += 1
            print line
        else:
            f2.write(line)
    
    print 'total number of lines = ' + str(ln)
    print 'total number of duplicate lines = ' + str(duplines)
    print 'total lines of real data = ' + str(ln - duplines)

            
    
    
