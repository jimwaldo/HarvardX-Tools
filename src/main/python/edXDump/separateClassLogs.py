#!/usr/bin/env python
"""
Take the log files for the various days, and separate them by class

This script will take all the log files for a particular server (one for each day)
that are in a particular directory (by server) and separate them into log files for
a given class. The entries are separated by the class identifier found in each log
entry, labeled by the course id in the context structure. 
Created on Feb 5, 2014

@author: waldo
"""
import os
import glob
import json
import csv
       
def addName(name, filedict, dirName):
    """
    Adds the name of a course to the dictionary of courses, and opens a log file 
    for the entries for that course
    """
    fname = name + '-' + dirName
    fout = open(fname, 'w')
    filedict[name] = fout
    
def getName(line):
    """
    Extracts the name of the course from the log entry. If no course name is 
    in the log entry, the log entry goes into the unknown class file
    """
    try:
        dcl = json.loads(line)
        cl = dcl['context']['course_id']
        cl = cl[cl.find('/') +1 : ]
        cl = cl.replace('/', '-')
        if cl == '':
            cl = 'unknown'
    except ValueError:
        cl = 'unknown'
    return cl
    
def getClassList():
    """
    Returns a dictionary of class names and number of log entries for that class.
    Finds out if there is a ClassList.csv file at the next level of the directory
    hierarchy, and if so reads that file and creates a dictionary of class name and
    log entry counts for the class. Otherwise, returns an empty dictionary. Note 
    that the ClassList.csv file will be written at the end of the extraction of
    class log entries.
    """
    cldict = {}
    if 'ClassList.csv' in os.listdir('..'):
        clfile = open('../ClassList.csv', 'rU')
        clreader = csv.reader(clfile)
        for cname, count in clreader:
            cldict[cname] = int(count)
        clfile.close()
    return cldict

def get_log_files():
    """
    Returns a sorted list of all of the daily files in the directory. Since the 
    files are sorted by date, the log entries encountered when reading through those
    files will be in time-stamp order.
    """
    fileList = glob.glob('20*.log')
    fileList.sort()
    return fileList

if __name__ == '__main__':
    courseDict = getClassList()
    filedict = {}
    dirName = os.getcwd()
    dirName = dirName[dirName.rindex('/')+1:]
    loglist = get_log_files()
    for logName in loglist:
        infile = open(logName, 'r')
        for line in infile:
            cName = getName(line)
            if cName not in filedict:
                addName(cName, filedict, dirName)
            filedict[cName].write(line)
            if cName not in courseDict:
                courseDict[cName] = 1
            else:
                courseDict[cName] += 1
        infile.close()
    
    for n in iter(filedict):
        filedict[n].close()
        
    clFile = csv.writer(open('../ClassList.csv', 'w'))
    for c in iter(courseDict):
        clFile.writerow([c, courseDict[c]])