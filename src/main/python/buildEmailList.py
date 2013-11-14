#!/usr/bin/env python
'''
Created on Nov 13, 2013

@author: waldo
'''
import demographics.userprofile as userp
import user
import sys
import csv

def split(name):
    spIn = name.rfind(' ')
    first = name[ :spIn]
    last = name[spIn + 1: ]
    return [first, last]

if __name__ == '__main__':
    csv.field_size_limit(sys.maxsize)
    ufile = csv.reader(open('users.csv','r'))
    udict = user.builddict(ufile)
    pfile = csv.reader(open('profiles.csv', 'r'))
    pdict = userp.builddict(pfile)
    
    outfile = csv.writer(open('mailAddresses.csv','w'))
    
    for uid in iter(udict):
        name = pdict[uid].name
        [first, last] = split(name)
        outfile.writerow([first, last, udict[uid].email])
