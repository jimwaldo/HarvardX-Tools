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
import user
import certificates
import course_enrollment

def compareUsers(d1, d2):
    retDict = {}
    for u in iter(d1):
        if u not in d2:
            retDict[u] = 'n'
    return retDict
            
ck_course = sys.argv[1]

dump2 = 'harvardx-2013-06-16'
dump1 = 'harvardx-2013-06-02'
userFile = '/' + ck_course + '/users.csv'
certFile = '/' + ck_course + '/certificates.csv'
enroll = '/' + ck_course + '/enrollment.csv'
uf1 = csv.reader(open(dump1 + userFile, 'r'))
uf2 = csv.reader(open(dump2 + userFile, 'r'))
cf1 = csv.reader(open(dump1 + certFile, 'r'))
cf2 = csv.reader(open(dump2 + certFile, 'r'))
ef1 = csv.reader(open(dump1 + enroll, 'r'))
ef2 = csv.reader(open(dump2 + enroll, 'r'))

u1dict = user.builddict(uf1)
u2dict = user.builddict(uf2)
c1dict = certificates.builddict(cf1)
c2dict = certificates.builddict(cf2)
e1dict = course_enrollment.builddict(ef1)
e2dict = course_enrollment.builddict(ef2)

OneNotTwo = compareUsers(u1dict, u2dict)
TwoNotOne = compareUsers(u2dict, u1dict)

for u in iter(OneNotTwo):
    if u in c1dict and c1dict[u].status =='downloadable':
        OneNotTwo[u] = 'y'

for u in iter(TwoNotOne):
    if u in c2dict and c2dict[u].status == 'downloadable':
        TwoNotOne[u] = 'y'

outfile = csv.writer(open('userDiff06020616' + ck_course +'.csv', 'w'))
outfile.writerow(['Users in 06/02 list but not in 06/16 list'])
outfile.writerow(['User id', 'Certificate granted', 'Date enrolled'])
for u in iter(OneNotTwo):
    if u in e1dict:
        signdate = e1dict[u].enroll_d
    else:
        signdate = ''
    outfile.writerow([u, OneNotTwo[u], signdate])

outfile.writerow(['Users in 06/16 list but not in 06/02 list'])
outfile.writerow(['User id', 'Certificate granted', 'Date enrolled'])
for u in iter(TwoNotOne):
    if u in e2dict:
        signdate = e2dict[u].enroll_d
    else:
        signdate = ''
    outfile.writerow([u, TwoNotOne[u], signdate])
                    


