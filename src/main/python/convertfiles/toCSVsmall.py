#!/usr/bin/env python

'''Convert an XML file to a CSV file, one row at a time

This script will convert an XML file that is a sequence of row values into
a CSV file. The conversion assumes that the XML is formatted as a series of
rows demarcated by <row> and </row> and that the values inside the row are
only one deep (which is the way that the XML files for course data from edX
are formatted). Unlike the toCSV.py conversion script, this script does
not attempt to parse the entire file. As such, it may not do as complete
a job in understanding the XML. When it is unable to parse a particular
value, it writes a null entry to the row.

'''
import xml.etree.ElementTree as ET
import sys
import csv

def findelestart(f):
    line = f.readline()
    while not ('<row>' in line) and not(len(line) == 0):
        line = f.readline()
    return line

def buildline(line, f):
    addline = f.readline();
    line += addline
    while ('</field>' not in addline and '/>' not in line):
        addline = f.readline()
        line += addline
        
    return line

def buildvalues(f):
    line = f.readline()
    retvals = []
    while not ('</row>' in line):
        if (not "</field>" in line and not '/>' in line):
            line = buildline(line, f)
        try:
            ele = ET.fromstring(line)
            val = ele.text
            if (isinstance(val,unicode)):
                val = val.encode("utf8")
            retvals = retvals + [val]
        except:
            retvals = retvals + [' ']
        line = f.readline()
    return retvals
        

outfile = csv.writer(open(sys.argv[2], 'w'))
infile = open(sys.argv[1], 'r')
while not (len(infile.readline()) == 0):
    curline = findelestart(infile)
    if len(curline) == 0:
        break
    rowvalues = buildvalues(infile)
    outfile.writerow(rowvalues)



