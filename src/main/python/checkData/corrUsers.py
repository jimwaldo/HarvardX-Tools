#!/usr/bin/env python
'''
Checks to insure that users appear in the enrollment and profiles file

Looks at the user, enrollment, and profile file in the directory in which 
the script is run to insure that all of the entries in the user file
have entries in the enrollment and profiles file, and that fall of the
entries in the profiles and enrollment file have entries in the user file.
'''


import csv
import user
import demographics.userprofile as uprofile
import course_enrollment as ce

csv.field_size_limit(1000000)
uIn = csv.reader(open('users.csv', 'r'))
uDict = user.builddict(uIn)

upIn = csv.reader(open('profiles.csv', 'r'))
upDict = uprofile.builddict(upIn)

ceIn = csv.reader(open('enrollment.csv', 'r'))
ceDict = ce.builddict(ceIn)

of = csv.writer(open('userDiffs.csv', 'w'))

of.writerow(['ids in user file, not in profiles file'])
for u in iter(uDict):
    if u not in upDict:
        of.writerow([u])

of.writerow(['ids in profiles file, not in user file'])
for p in iter(upDict):
    if p not in uDict:
        of.writerow([p])

of.writerow(['ids in user file, not in enrollment file'])
for u in iter(uDict):
    if u not in ceDict:
        of.writerow([u])

of.writerow(['ids in enrollment file, not in user file'])
for e in iter(ceDict):
    if e not in uDict:
        of.writerow([u])
        
    
