#!/usr/bin/env python

import user
import certificates
import os
import csv


def getFileName(prompt):
    while (True):
        fname = raw_input("Please enter file name for " + prompt + ' : ')
        if os.path.exists(fname):
            return fname
        else:
            print ("file entered does not exist, please retry")

if __name__ == '__main__':
    f1name = getFileName('Enter name of the user file')
    f1 = csv.reader(open(f1name, 'r'))
    f2name = getFileName('Enter the name of the certificates file')
    f2 = csv.reader(open(f2name, 'r'))
    udict = user.builddict(f1)
    cdict = certificates.builddict(f2)
    out1 = open('allmail', 'w')
    out2 = open('certMail', 'w')
    for u in iter(udict):
        out1.write(udict[u].email + '\n')
        if u in cdict:
            out2.write(udict[u].email + '\n')


        

