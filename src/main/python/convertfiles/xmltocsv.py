'''
Utilities to convert edX data from XML files to CSV files


Created on Feb 24, 2013

@author: waldo
'''
import xml.etree.ElementTree as ET
import sys
import csv

if __name__ == '__main__':
    pass

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
            retvals = retvals + ['']
        line = f.readline()
    return retvals
        
def xmltocsviter(fnamein, fnameout):
    outfile = csv.writer(open(fnameout, 'w'))
    infile = open(fnamein, 'r')
    while not (len(infile.readline()) == 0):
        curline = findelestart(infile)
        if len(curline) == 0:
            break
        rowvalues = buildvalues(infile)
        outfile.writerow(rowvalues)

def xmltocsvfull(fnamein, fnameout):
    outfile = csv.writer(open(fnameout, 'w'))
    tree = ET.parse(fnamein)
    root = tree.getroot()

    for row in root:
        writerow = []
        for child in row:
            if (isinstance(child.text, unicode)):
                child.text = child.text.encode('utf8')
            writerow = writerow + [child.text]
        outfile.writerow(writerow)

            
def scrubcsv(fnamein, fnameout, i):
    csv.field_size_limit(100000000)
    infile = csv.reader(open(fnamein, 'r'))
    outfile = csv.writer(open(fnameout, 'w'))
    for row in infile:
        if len(row) == i:
            outfile.writerow(row)
            
