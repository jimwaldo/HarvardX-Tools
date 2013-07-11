#!/usr/bin/env python
'''
Get all of the log files in the server directories and separate them by class

Gets all of the .log files in a directory, and separates the entries into separate
logs for each class. The classes are determined by the edX numbering. Any entry that
does not have a class identifier in the interaction URL is placed into a separate
file marked as unknown. The resulting files are named by concatenating the class
name with the server name and ending with a .log extension. 

Note that this will create empty files for classes that have no log entries. These
are removed as part of the log processing script later in the process.

The program takes as an argument the name of the server that generated the logs.
'''
import sys
import glob

classes = ['AI121x', 'AI122x', 'CB22x', 'CS50x', 'CS50', 'ER22x', 'GSE1x','HLS1', 'HMS214x', 'MCB80x', 'PH201x', 'PH207x', 'PH278x', 'SPU27x', 'SW12SONDx', 'SW12x' ]

def get_log_files():
    fileList = glob.glob('*.log')
    fileList.sort()
    return fileList

def openOutputFiles(server):
    filedict = {}
    for cname in classes:
        cdname = cname + '_' + server + '.log'
        cfile = open(cdname, 'w')
        filedict[cname] = cfile
    return filedict

serverName = sys.argv[1]
logList = get_log_files()

filedict = openOutputFiles(serverName)
unknownf = open('unknown'+serverName + '.log', 'w')

for logName in logList:
    print logName
    infile = open(logName, 'r')
    for line in infile:
        written = False
        for cname in classes:
            if (cname in line):
                filedict[cname].write(line)
                written = True
                break
        if (not written):
            unknownf.write(line)
    infile.close()
