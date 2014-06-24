#!/usr/bin/env python
'''
Creates a file listing all of the ip addresses associated with a user in a log file.

Given a log file, creates a dictionary keyed by username with contents a list of all of 
the ip addresses associated with the user in that log file. Writes a csv file with the
form username, list-of-ips. The log file to be read and the output file are arguments
to the command line.
Created on Nov 3, 2013

@author: waldo
'''

import sys
import json
import csv

if __name__ == '__main__':
    logFile = sys.argv[1]
    nameIpDict = {}
    fin = open(logFile, 'r')
    for line in fin:
        dline = json.loads(line)
        uname = dline['username']
        ipAddr = dline['ip']
        if uname in nameIpDict:
            if ipAddr not in nameIpDict[uname]:
                nameIpDict[uname].append(ipAddr)
        else:
            nameIpDict[uname] = [ipAddr]
    outfile = csv.writer(open(sys.argv[2], 'w'))
    for n in sorted(iter(nameIpDict)):
        outfile.writerow([n, nameIpDict[n]])
    
        