#!/usr/bin/env python
'''
Using a list of classes found in a file, separate the edX supplied research data files
so that they are in different directories, one per class

This script runs over the flat directory supplied by edX and moves files into directories
for each class. The types of data files is hard-coded into the script, which is probably
not a great idea, but can be changed in the routine makeDestName. The routine that
does the actual moving will check and not move directories and will remove zero-length
files rather than move them. The script assumes that the list of classes is in the file
WeeklyClassList in the directory in which the script is run.

Created on Sep 21, 2013

@author: waldo
'''
import glob
import buildClassList
import os
import shutil
import convertfiles.sqltocsv as conv


def makeDestName(fileName):
    '''
    Determine the name of the file as it will appear after being moved into the 
    directory for the class. Currently this follows a set pattern, where the data
    files are forum.mongo, and then .sql files for users, profiles, student modules,
    course enrollment, and certificates. This will need to be changed when different
    data files are produced.
    '''
    retName = ''
    if '.mongo' in fileName:
        retName = 'forum.mongo'
    elif 'profile' in fileName:
        retName = 'profiles.sql'
    elif 'certificate' in fileName:
        retName = 'certificates.sql'
    elif 'studentmodule' in fileName:
        retName = 'studentmodule.sql'
    elif 'auth_user' in fileName:
        retName = 'users.sql'
    elif 'courseenrollment' in fileName:
        retName = 'enrollment.sql' 
    elif 'user_id_map' in fileName:
        retName = 'user_id_map.sql'
    elif 'course_structure' in fileName:
        retName = 'course_structure.json'
    elif 'course' in fileName and 'xml.tar.gz' in fileName:
        retName = 'course.xml.tar.gz'
    else:
        retName = fileName
    return retName

    
def moveFiles(forCourse, flist):
    '''
    Move files from the flat directory to a directory that holds all the data for
    a single class. The routine will not move directories, and removes zero length
    files rather than moving them. If the file has the string 'edge' it is moved
    to a directory for the edge data, otherwise it is assumed to be a full edX course.
    '''
    for f in flist:
        if os.path.isdir(f):
            continue
        if 0 == os.path.getsize(f):
            os.remove(f)
            continue
        destdir = forCourse
        if 'edge' in f:
            destdir += '-edge'
        destname = makeDestName(f)
        dest = destdir + '/' + destname
        print 'about to move', f, 'to', dest
        os.rename(f, dest)
     

if __name__ == '__main__':
    classList = buildClassList.readList(open('weeklyClassList', 'r'))
    for c in classList:
        os.mkdir(c)
        os.mkdir(c + '-edge')
        if 'edge' not in c:
            flist = glob.glob('*' + c + '*')
            moveFiles(c, flist)
            
    convertList = glob.glob('*/*.sql')
    for c in convertList:
        print 'Converting file', c
        toBuild = c[:-3] + 'csv'
        conv.convertFile(c, toBuild)
        
        
 