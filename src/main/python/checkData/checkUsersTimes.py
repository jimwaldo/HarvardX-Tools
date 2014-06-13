#!/usr/bin/env python
'''
Compare the user files for a class over multiple weeks, and determine if any of those not
active in both weeks were awarded a certificate, and the date of enrollment of those who
are in one list but not the other

Looks at the user, enrollment, and certificate files in multiple directories for a class,
and produces a list of those users that are in one user list and not the other. For those
users, the script looks into the enrollment file to determine when the student enrolled,
and at the certificates file to see if the student was awarded a certificate.

Currently, the class for which this is done is specified as a command-line argument. The
weeks compared is hard-coded.

'''

import os
import sys
import csv
from classData import certificates, user, course_enrollment

def compareUsers(d1, d2):
    retDict = {}
    for u in iter(d1):
        if u not in d2:
            retDict[u] = 'n'
    return retDict
            
if __name__ == '__main__':
    ck_course = sys.argv[1]
    wk1 = sys.argv[2]
    wk2 = sys.argv[3]
    week1 = wk1 + '/' + ck_course
    week2 = wk2 + '/' + ck_course
    userFile = '/users.csv'
    certFile = '/certificates.csv'
    enroll = '/enrollment.csv'
    uf1 = csv.reader(open(week2 + userFile, 'r'))
    uf2 = csv.reader(open(week1 + userFile, 'r'))
    cf1 = csv.reader(open(week2 + certFile, 'r'))
    cf2 = csv.reader(open(week1 + certFile, 'r'))
    ef1 = csv.reader(open(week2 + enroll, 'r'))
    ef2 = csv.reader(open(week1 + enroll, 'r'))
    u1dict = user.builddict(uf1)
    u2dict = user.builddict(uf2)
    c1dict = certificates.builddict(cf1)
    c2dict = certificates.builddict(cf2)
    e1dict = course_enrollment.builddict(ef1)
    e2dict = course_enrollment.builddict(ef2)
    OneNotTwo = compareUsers(u1dict, u2dict)
    TwoNotOne = compareUsers(u2dict, u1dict)
    for u in iter(OneNotTwo):
        if u in c1dict and c1dict[u].status == 'downloadable':
            OneNotTwo[u] = 'y'
    
    for u in iter(TwoNotOne):
        if u in c2dict and c2dict[u].status == 'downloadable':
            TwoNotOne[u] = 'y'
    
    outfile = csv.writer(open('userDiff06020616' + ck_course + '.csv', 'w'))
    outfile.writerow(['Users in ' + wk1 + ' list but not in ' + wk2 + ' list'])
    outfile.writerow(['User id', 'Certificate granted', 'Date enrolled'])
    for u in iter(OneNotTwo):
        if u in e1dict:
            signdate = e1dict[u].enroll_d
        else:
            signdate = ''
        outfile.writerow([u, OneNotTwo[u], signdate])
    
    outfile.writerow(['Users in ' + wk2 + ' list but not in ' + wk1 + ' list'])
    outfile.writerow(['User id', 'Certificate granted', 'Date enrolled'])
    for u in iter(TwoNotOne):
        if u in e2dict:
            signdate = e2dict[u].enroll_d
        else:
            signdate = ''
        outfile.writerow([u, TwoNotOne[u], signdate])

                    


