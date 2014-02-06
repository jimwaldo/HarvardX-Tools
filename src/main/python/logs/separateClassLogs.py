#!/usr/bin/env python
'''
Created on Feb 5, 2014

@author: waldo
'''
import os
import glob
import json
       
def addName(name, filedict, dirName):
    fname = name + '-' + dirName
    fout = open(fname, 'w')
    filedict[name] = fout
    
def getName(line):
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
    
    
def get_log_files():
    fileList = glob.glob('20*.log')
    fileList.sort()
    return fileList

if __name__ == '__main__':
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
        infile.close()
    
    for n in iter(filedict):
        filedict[n].close()