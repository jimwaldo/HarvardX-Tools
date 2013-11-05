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

Also note that there are some hacks to deal with classes that have multiple runs
that may appear in the same log file. Some of these can be distinguished by the
log entry, but others have to be placed by default in one class run or another, in
a fashion that is not currently very well justified by the data.

The program takes as an argument the name of the server that generated the logs.
'''
import sys
import glob

classes = ['AI12.1x', 'AI12.2x', 'CB22.1x', 
           'CB22x', 'CS50x', 'CS50', 'ER22x', 
           'GSE1x', 'HKS211.1x','HKS_211', 'HDS1544',
           'HLS1','HMS214x', 'ITCx', 'MCB80.1x', 
           'PH201x', 'PH207x', 'PH278x', 'PH278X',
           'HS221', 'SPU17x', 'SPU27x', 'SPU27X', 'SW12', ]

class fileOut(object):
    
    def __init__(self, fname):
        self.fname = fname
        self.fout = None
        
    def write(self, st):
        if self.fout == None:
            self.fout = open(self.fname, 'w')
        self.fout.write(st)
        
def get_log_files():
    fileList = glob.glob('*HarvardX.log')
    fileList.sort()
    return fileList

def openOutputFiles(server):
    filedict = {}
    for cname in classes:
        if cname == 'CS50x':
            cname = 'CS50x-2012'
            cdname = cname + server + '.log'
            cfile = fileOut(cdname)
            filedict[cname] = cfile
            cname = 'CS50x-2014'
            cdname = cname + server + '.log'
            cfile = fileOut(cdname)
            filedict[cname] = cfile
        elif cname == 'SW12':
            cname = 'SW12_Oct'
            cdname = cname + server + '.log'
            cfile = fileOut(cdname)
            filedict[cname] = cfile
            cname = 'SW12_SOND'
            cdname = cname + server + '.log'
            cfile = fileOut(cdname)
            filedict[cname] = cfile
        elif cname == 'HKS_211':
            filedict[cname] = filedict['HKS211.1x']
        elif cname == 'PH278X':
            filedict[cname] = filedict['PH278x']
        else:
            cdname = cname + '_' + server + '.log'
            cfile = fileOut(cdname)
            filedict[cname] = cfile
    
    return filedict

def parse_cname(cname, line):
    if cname == 'CS50x':
        if '2014' in line:
            cname = 'CS50x-2014'
        else:
            cname = 'CS50x-2012'
    elif cname =='SW12':
        if '2013_SOND' in line:
            cname = 'SW12_SOND'
        else:
            cname = 'SW12_Oct'
    return cname

if __name__ == '__main__':
    serverName = sys.argv[1]
    logList = get_log_files()

    filedict = openOutputFiles(serverName)
    unknownf = open('unknown'+serverName + '.log', 'w')

    for logName in logList:
        infile = open(logName, 'r')
        for line in infile:
            written = False
            for cname in classes:
                if (cname in line):
                    cname = parse_cname(cname, line)
                    filedict[cname].write(line)
                    written = True
                    break
            if (not written):
                unknownf.write(line)
        infile.close()
