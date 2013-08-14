#!/usr/bin/env python

'''
Build a course roster, with basic demographic information
'''

import glob
import csv
import sys
import user
import demographics.userprofile as profile
import ipGeoloc as geo

class rosterLine(object):
    def __init__(self, sid, name, uname, maddr, cnt, age, ed, gend):
        self.sid = sid
        self.name = name
        self.uname = uname
        self.maddr = maddr
        self.cnt = cnt
        self.age = age
        self.ed = ed
        self.gender = gend
        
def buildRosterDict(proD, udict, locD):
    '''
    Build a class roster from a profile dictionary and a dictionary of country locations
    
    The dictionary created will be indexed by the student id, and will contain lines 
    with the student id, student name, country (as determined by ip address), age, 
    education level (in a human readable form), and gender.
    '''
    rDict = {}
    for p in iter(proD):
        if p in locD:
            cnt = locD[p]
        else:
            cnt = 'id not in loc file'
        if p in udict:
            uname = udict[p].username
            maddr = udict[p].email
        else:
            uname = 'Not in user file'
        if proD[p].yob.isdigit():
            age = 2013 - int(proD[p].yob)
        else:
            age = 'unspecified'
        edu = proD[p].ledu
        edisc = 'unknown'
        if edu is not None:
            edisc = profile.trans_ledu(edu)
        rl = rosterLine(p, proD[p].name, uname, maddr, cnt, age,
                    edisc, proD[p].gender)
        rDict[p] = rl
    return rDict

def readRoster(filein):
    '''
    Create a class roster dictionary from a file created by writeRoster
    
    Reads the file named by the input parameter. The assumption is that this file is 
    a .csv file in the form written by writeRoster. The first line is skipped (since it
    is assumed to be a header), and then a dictionary, indexed by student id, is created 
    with name, country, age, education level, and gender. Note that the education level
    will be a human-readable version of the level, not the encoding used in the profile
    file.
    '''
    ofile = open(filein, 'r')
    rfile = csv.reader(ofile)
    rfile.next()
    retDict = {}
    for l in rfile:
        [sid, name, uname, maddr, cnt, age, edu, gender] = l
        rl = rosterLine(sid, name, uname, maddr, cnt, age, edu, gender)
        retDict[sid] = rl
    ofile.close()
    return retDict

def writeRoster(rDict, filein):
    '''
    Write a roster dictionary to a .csv file
    
    Write a class roster dictionary to a .csv file named by the input parameter. 
    '''
    ofile = open(filein, 'w')
    rf = csv.writer(ofile)
    rf.writerow(['Student ID', 'Name', 'User Name', 'Email', 'Country', 'Age', 'Education Level', 'Gender'])
    for s in iter(rDict):
        wl = rDict[s]
        rf.writerow([wl.sid, wl.name, wl.uname, wl.maddr, wl.cnt, wl.age, wl.ed, wl.gender])
    ofile.close()
    

if __name__ == '__main__':     
    csv.field_size_limit(sys.maxsize)
    cl_name = sys.argv[1]

    proDict = profile.builddict(csv.reader(open(cl_name + '/profiles.csv', 'r')))
    uDict = user.builddict(csv.reader(open(cl_name + '/users.csv', 'r')))
    loc_name = sys.argv[2]
    locDict = geo.readIdToLoc(loc_name)
    rDict = buildRosterDict(proDict, uDict, locDict)
    writeRoster(rDict, cl_name + '/class_roster.csv')
    