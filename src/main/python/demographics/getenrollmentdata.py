#!/usr/bin/env python
"""
This program will construct a table of when the students of a course registered,
and will track the self-reported gender of those students. The result is a csv
file that contains the date of enrollment, the number of self-reported males,
the number of self-reported females, and the number who did not report, along
with the total number that registered on that day. A final entry will give
totals for the three possible gender choices (M, F, no report) and the total for
the course.

Usage:
    getenrollmentdata.py file1 file2 file3
    
    where: 
    file1 is a csv representation of the student demographic information (user_profile),
    file2 is a csv representation of the course enrollment date (courseenrollent)
    file3 is a csv file that will be written with the enrollment information by day

Created on Feb 18, 2013

@author: waldo
"""

from classData import userprofile
import csv
import sys
import logging

if __name__ == '__main__':
    pass

class enrollday:
    def __init__(self):
        self.m = 0
        self.f = 0
        self.n = 0
        self.t = 0



def buildenrolldict(e, profiles):
    retdict = {}
    lineno = 0;
    for line in e:
        lineno += 1
        if len(line) != 4:
            logging.warning('bad enrollment line at ' + str(lineno))
            continue
        [rid, uid, cid, date] = line
        if uid not in profiles:
            continue
        day = date[:date.find(' ')]
        gender = profiles[uid].gender
        if day not in retdict:
            retdict[day]= enrollday()
        if gender == 'm':
            retdict[day].m += 1
        elif gender == 'f':
            retdict[day].f += 1
        else :
            retdict[day].n += 1
        retdict[day].t += 1
    return retdict
            
        
csv.field_size_limit(1000000000)
f = csv.reader(open(sys.argv[1], 'r'))
profdict = userprofile.builddict(f)
e = csv.reader(open(sys.argv[2], 'r'))
enrdict = buildenrolldict(e, profdict)
it = sorted(enrdict.keys())
outfile = csv.writer(open(sys.argv[3], 'w'))
mt = ft = nt = 0
outfile.writerow(['Enroll Date', 'Male', 'Female', 'Unspecified', 'Total'])
for date in it:
    rec = enrdict[date]
    outfile.writerow([date, rec.m, rec.f, rec.n, rec.t])
    mt += rec.m
    ft += rec.f
    nt += rec.n
    
outfile.writerow(['', mt, ft, nt, mt+ft+nt])
        
