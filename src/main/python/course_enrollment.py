'''
Object definition and utility functions for the course enrollment file

Contains a definition of the course_enrollment object, that holds all of the
information found in the course enrollment file. There is a function that will
build a dictionary, keyed by user id, that holds the information. There is also
a function that will scrub badly-formed entries from the file.

Created on Mar 17, 2013

@author: waldo
'''
import logging
from convertfiles import xmltocsv

class course_enrollment(object):
    '''
    A representation of the state kept concerning a student's enrollment
    
    This object encapsulates the time of enrollment for a student. There isn't
    much here other than the student id, the course id, and the date of enrollment
    
    '''


    def __init__(self, id, course_id, enroll_d):
        '''
        Constructor for an object containing the enrollment state
        
        Note that the id that is only relevant within the file is not part of this
        object.
        
        '''
        self.id = id
        self.course_id = course_id
        self.enroll_d = enroll_d
        
def builddict(f):
    '''
    Build a dictionary of the enrollment date for a student
    
    The dictionary that is returned by this function is indexed by student id.
    The internal id that is stored in the raw data file is dropped, as it has no
    meaning outside of this file.
    
    Parameters
    -----------
    f: csv.reader
        An open csv reader object that contains the course enrollment data
    '''
    retdict = {}
    lineno = 0
    for line in f:
        lineno += 1
        if len(line) != 4:
            logging.warning('bad row size at line ' + str(lineno))
            continue
        [id, user_id, course_id, enrolld] = line
        rec = course_enrollment(user_id, course_id, enrolld)
        retdict[user_id] = rec
        
    return retdict

def scrubstate(f1, f2):
    '''
    Clean up the state of a course enrollment csv file
    
    Reads through a csv file containing the course enrollment data, removing any
    lines that are of the wrong size. Produces a scrubbed csv file
    
    Parameters
    --------------
    f1: csv reader
        An open csv reader, containing the data to be cleaned up
    f2: csv writer
        An open csv writer, that will take all of the lines of the right 
        size
    '''
    
    xmltocsv.scrubcsv(f1, f2, 4)
        
