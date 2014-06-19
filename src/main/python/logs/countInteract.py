#!/usr/bin/env python
"""
Count the number of interactions in a log file for each user. 

Produces a pair of output files. The main file will just have the
count of interactions from a log file for each user, along with a cound of the number
of different days that the interactions took place. The detail file includes the 
different interactions, as well.
 
"""

import json
import sys
import csv

class InteractRec:
    def __init__(self):
        self.totalInt = 0
        self.diffDays = 0
        self.idic = {}

    def addRec(self, when):
        self.totalInt += 1
        if (when in self.idic):
            self.idic[when] += 1
        else:
            self.diffDays += 1
            self.idic[when] = 1

if __name__ == '__main__':
    f1 = open(sys.argv[1], 'r')
    f2 = csv.writer(open(sys.argv[2] + '.csv', 'w'))
    f3 = csv.writer(open(sys.argv[2] + 'detail.csv', 'w'))
    dc = json.JSONDecoder()
    interAct = {}
    for line in f1:
        dcl = dc.decode(line)
        user = dcl['username']
        if (user not in interAct):
            interAct[user] = InteractRec()
        dt = dcl['time']
        d = dt[:dt.find('T')]
        interAct[user].addRec(d)
    
    for user in interAct:
        f2.writerow((user, interAct[user].totalInt, interAct[user].diffDays))
        i = interAct[user].idic
        for d in i:
            f3.writerow((user, d, i[d]))

