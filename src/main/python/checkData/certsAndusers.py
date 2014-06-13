#!/usr/bin/env python

'''
Looks for differences between the user listed in the users file and those in the certificates file.

In particular, looks for any users not found in the users file who have received a certificate. This
was used for basic sanity testing on the invariant that if a user received a certificate, he or she
should also be in the users file. There are odd cases where this may not be the case, caused by the
habit of the edX group to delete a user (which may have been changed, we have asked for this), but
if there are large numbers (order 10s) then something is probably wrong.
'''
import csv
from classData import certificates, user

if __name__ == '__main__':
    ufile = csv.reader(open('users.csv', 'r'))
    udict = user.builddict(ufile)
    cfile = csv.reader(open('certificates.csv', 'r'))
    cDict = certificates.builddict(cfile)
    certsMissing = []
    for c in iter(cDict):
        if (cDict[c].status == 'downloadable') and (c not in udict):
            certsMissing.append(c)
    
    if len(certsMissing) > 0:
        print 'found ' + str(len(certsMissing)) + ' certificates with no associated user'
        outfile = csv.writer(open('certsAndusers.csv', 'w'))
        outfile.writerow(['Missing user ids that have certificates'])
        for u in certsMissing:
            outfile.writerow([u])


                   

