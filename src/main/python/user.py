#!/usr/bin/env python
'''
Object definition and utility functions for the course users (students) file

Contains a definition of a user object, that holds all of the information
found in the users file for each entry. There is a function that will build
a dictionary, keyed by the user id, for all of those entries. There is also
a function that will remove any mal-formed entries in the file.

Created on Feb 20, 2013

@author: waldo
'''

from convertfiles import xmltocsv
import json

class user(object):
    '''
    Representation of the data stored in the auth_user files
    
    This object contains all of the fields that are reported in a single entry
    from the auth_user extraction from the databases. These fields are self-
    reported, and not all of the fields are required, so they are often not all
    filled in. Further, a number of these fields are no longer used or reported,
    and so are ignored.
     
    '''


    def __init__(self, id, username,
                 email, is_staff, is_active, is_super,
                 last_l, date_j):
        '''
        Constructor for a user object
        
        This constructor creates and initializes the user object, using only the
        fields that are currently active.
        
        '''
        self.id = id
        self.username = username
        self.email = email
        self.is_staff = is_staff
        self.is_active = is_active
        self.is_super = is_super
        self.last_l = last_l
        self.data_j = date_j
     
def builddict(f):
    '''
    Build a dictionary of user information, indexed by user_id
    
    Builds a dictionary of user information from a csv file. If any line in the
    file is not of the correct length, the line number will be printed and the
    information discarded.
    
    Parameters
    ---------------
    f: csv.reader
    
        An open csv.reader containing the authorized user data
        
    '''
    
    retdict = {}
    lineno = 0;
    for line in f:
        if len(line) != 22:
            print ('bad line length at line' + str(lineno))
            print ('expected 22, got ' + str(len(line)))
            continue
        [id, username, first, last, em, passwd, staff, active, \
        super, lastl, djoin, status, emkey, avatar, country, shc, \
        dob, inttags, igntags, emailt, displayt, concecdays] = line
        if id not in retdict:
            rec = user(id, username, em, staff,
                        active, super, lastl, djoin)
        retdict[id] = rec
            
    return retdict
    
def scrubfile(f1, f2):
    '''
    Traverse a csv file, copying lines with the right set of entries to a second csv file
    
    Parameters:
    --------------
    f1: csv.reader
        An open csv.reader object, containing the raw data
    f2: csv.writer
        An open csv.writer object, to which the scrubbed data will be written
    '''
    xmltocsv.scrubcsv(f1, f2, 22)
    

        
