#!/usr/bin/env python
"""
Produce a list of all users, and the number of classes the user is in. 

Run from a directory that contains a set of directories of class data for different
classes, find all of the users and count the number of classes each user is in. This 
also uses a user->country file of the form supplied by edX to give the country of 
each of the users; the name of this file needs to be given as the first argument to 
the program on the command line.

"""
import glob
from classData import user
import csv
from classData import ipGeoloc as loc
import sys

class userClasses:
    def __init__(self, uname, className):
        self.numClasses = 1
        self.uname = uname
        self.country = ''
        self.classList = [className]
    

if __name__ == '__main__':    
    geoFile = csv.reader(open(sys.argv[1], 'r'))
    geoDict = loc.builddict(geoFile)
    fList = glob.glob('*/users.csv')
    classDict = {}
    for d in fList:
        filein = open(d, 'r')
        fin = csv.reader(filein)
        cName = d[ :10]
        fin.next()
        udict = user.builddict(fin)
        for u in iter(udict):
            if u in classDict:
                classDict[u].numClasses += 1
                classDict[u].classList.append(cName)
                if udict[u].username != classDict[u].uname:
                    classDict[u].uname = 'Duplicate user name'
            else:
                classDict[u] = userClasses(udict[u].username, cName)
                if udict[u].username in geoDict:
                    classDict[u].country = geoDict[udict[u].username]
        
        filein.close()
    
    outf = csv.writer(open('studentClassList.csv', 'w'))
    outf.writerow(['user Id', 'User name', 'country', 'number of classes', 'classes'])
    for u in iter(classDict):
        outf.writerow([u, classDict[u].uname, classDict[u].country, classDict[u].numClasses, classDict[u].classList])
