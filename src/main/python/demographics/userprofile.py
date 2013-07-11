#!/usr/bin/env python
'''
Utilities for a CSV version of the edX auth_studentprofile data

The object built by the profile constructor will include all of the data
that is currently gathered by edX, ignoring some of the fields that have
not been used since the initial course offerings. There is also a function
that will build a dictionary, indexed by user_id, of all of these objects.
Finally, there is a function that will scrub a CSV file of all of the entries
that don't have the right number of fields in each row; this is an outcome
of the dirty data that we get from edX

Created on Feb 18, 2013

@author: waldo
'''
import csv
from convertfiles import xmltocsv
import logging

class profile:
    '''
    Representation of the data contained in the auth_userprofile data dumps
    
    This class contains representations of the interesting data in the auth_userprofile files
    from the edX dumps. There is also a utility function that will build a dictionary, keyed
    by the user_id, for this information.
    '''

    def __init__(self, user_id, name, gender, maddr, yob, ledu, goal, allowcert):
        '''
        Constructor
        
        Note that all of the information, other than the user id, is self-reported and
        not checked. It may also be left blank. 
        '''
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.maddr = maddr
        self.yob = yob
        self.ledu = ledu
        self.goal = goal
        self.allowcert = allowcert
        
        
def builddict(f):
    '''
    Builds a dictionary of the student profile records in a CSV file
    
    This function takes an already opened CSV file containing the student profile
    data, and builds and returns a dictionary of that information indexed by
    user_id. If there are multiple records in the CSV file for a single user_id,
    the data from the last of those records will be used to populate the dictionary
    
    Some of the fields that are in the .csv file are no longer used or collected, and 
    so are not passed to the profile object that is stored in the dictionary. These
    include the location (loc) and the language (lang).
    
    Note that if the line read is of the wrong length (corrupt data), a warning is 
    logged and the line is not added to the dictionary. Such lines can be removed from
    the csv file by running scrubprofile(). The first id in the csv file, which is 
    only meaningful in the context of this file, is not added to the dictionary
    
    Parameters
    -----------------
    f: csv.reader 
    file containing the student profiles, one per line
    '''
    retdict = {}
    lineno = 0
    for row in f:
        lineno += 1
        if (len(row) != 13):
            logging.warning('bad row size at line ' + str(lineno))
        else:
            [i, userid, name, lang, loc, meta, cw, gender, ma, yob, loe, gl, ac] = row
            info = profile(userid, name, gender, ma, yob, loe, gl, ac)
            retdict[userid] = info
            
    return retdict

def scrubprofile(f1, f2):
    '''
    Scrubs a CSV file of student profile data, removing lines of the wrong size
    
    Parameters
    ------------------
    f1: csv.reader
        An open csv reader containing the student profile data
    f2: csv.writer
        An open csv writer that will have the scrubbed data written to it
    
    '''
    xmltocsv.scrubcsv(f1, f2, 13)
    
def trans_ledu(ledu):
    '''
    Translates the level of education code to a human-readable string
    '''
    retStr = 'unknown or unsupplied'
    if ledu == 'p_se':
        retStr = 'Ph.D. in STEM'
    elif ledu == 'p_oth':
        retStr = 'Ph.D. in non-STEM field'
    elif ledu == 'm':
        retStr = 'Masters or professional degree'
    elif ledu == 'b':
        retStr = 'Bachelors degree'
    elif ledu == 'hs':
        retStr = 'Secondary/high school'
    elif ledu == 'jhs':
        retStr = 'Junior high school'
    elif ledu == 'el':
        retStr = 'Elementary school'

    return retStr

        
