#!/usr/bin/env python
"""
Extracts the number of ip addresses, and the number of log events associated with that address,
in a log file. Currently this will write the ip address and their total counts to a csv file, 
given either as an argument to the program or input by the user interactively. The log file
can be given as the (first) argument to the program, or entered interactively.

Usage: getIP {logfile, output.csv}


"""
import json
import csv
import sys
import utils

def getFileNames():
    if len(sys.argv) > 2:
        inName = sys.argv[1]
        outName = sys.argv[2]
    else:
        inName = utils.getFileName('Enter the name of the log file : ')
        outName = utils.getNewFileName('Enter name of the new file for output : ')
    return inName, outName

if __name__ == '__main__':
    inName, outName = getFileNames()
        
    inFile = open(inName, 'r')
    outfile = csv.writer(open(outName, 'w'))
    
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
