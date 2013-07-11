#!/usr/bin/env python

'''
Object definition and utility functions for course certificate file

Contains a definition of the certificate object, that holds all of the information
found in the certificates file for each entry. There is a method that will clean up
the file, removing any mal-formed entries, and a more useful function that will build
a dictionary, indexed by the user id, of the information in the file.
Created on Feb 20, 2013

@author: waldo
'''
import convertfiles.xmltocsv
import logging

class cert(object):
    '''
    Hold the information from the course_certificates data dump files
    
    This object reflects all of the fields held in the course_certificates
    data dump file, whether interesting or not. There is also a utility
    function to build a dictionary of all of the information, keyed by
    user_id, and a function that will remove all of the lines in a csv file
    for the certificates that are not of the correct length.
    '''


    def __init__(self, uid, durl, grade, courseid, key, distinction, status, \
                 ver_uuid, down_uuid, name, cdate, mdate, ereason):
        '''
        Constructor
        '''
        self.uid = uid
        self.download_url = durl
        self.grade = grade,
        self.courseid = courseid
        self.key = key
        self.distinction = distinction
        self.status = status
        self.ver_uuid = ver_uuid
        self.down_uuid = down_uuid
        self.name = name
        self.cdate = cdate
        self.mdate = mdate
        self.error_reason = ereason
        
        
def builddict(f):
    '''
    Construct a dictionary of certificate recipients, keyed by the id of the recipient
    
    The dictionary constructed by this function will contain a certificate object, keyed
    by the id of the recipient. If a line is read that is of the wrong size, a warning 
    is logged.
    
    Note that the second field of the raw csv file is ignored; this field is an id that
    is only meaningful in the context of this file. The id in the first field is the one
    that can be used to identify the student in other data files in this course (and in
    others, if they use the same edX registration). 
    
    Parameters
    -----------
    f: csv.reader 
        An open reader containing the information about the certificate recipients
    '''
    retdict = {}
    lineno = 0
    for row in f:
        lineno += 1
        if (len(row) != 14):
            logging.warning("bad line at " + str(lineno))
        else:
            [uid, ignore, durl, grade, cid, key, dist, stat, vuid, duid, name, cd, md, er] = row
            if uid not in retdict:
                rec = cert(uid, durl, grade, cid, key, dist, stat, vuid, duid, name, \
                            cd, md, er)
            retdict[uid] = rec
            
    return retdict

def scrubfile(f1, f2):
    '''
    Traverse a csv file, copying lines with the right set of entries to a second csv file
    
    '''
    convertfiles.xmltocsv.scrubcsv(f1, f2, 14)
            
