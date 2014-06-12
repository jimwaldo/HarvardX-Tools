#!/usr/bin/env python

"""
Find and report on duplicate lines in an edX log file

Reads the edX log file supplied as the first parameter. Building a dictionary
keyed by a concatenation of the username and time of the log entry, compares any 
two lines with the same key for equivalence. If they are the same, increments the 
count of duplicate lines and prints out the contents of the line, along with the 
sequence number of the duplicated line and the sequence number of the line it
duplicates. 

At the end of the run, prints out the number of log lines read, the number of 
duplicate lines found, and the number of non-duplicate lines.

If duplicate lines are found, they can be eliminated by running the script
cleanLogDups.py
"""
import json
import sys

class Line(object):
    def __init__(self, lineNo, lineCont):
        self.line = lineNo
        self.content = lineCont


linedict = {}

f1 = open(sys.argv[1], 'r')
ln = 0;
duplines = 0;

dc = json.JSONDecoder()

for line in f1:
    ln += 1;
    dl = dc.decode(line)
    key = dl['time'] + dl['username']
    if key not in linedict:
        lo = Line(ln, line)
        linedict[key] = lo
    else:
        if linedict[key].content == line:
            duplines += 1
            print line
            print 'line no ' + str(lo) + 'duplicates line no ' + str(linedict[key].line)

print 'total number of lines = ' + str(ln)
print 'total number of duplicate lines = ' + str(duplines)
print 'total lines of real data = ' + str(ln - duplines)
            
    
    
