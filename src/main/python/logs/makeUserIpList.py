#!/usr/bin/env python
'''
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
    
        