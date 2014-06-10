'''
Object definition and utility funcitons for the course student state data dumps

Contains a definition of a coursestudentstate object, which contains all of the 
information exported in the coursestudentstate files from edx. Also contains a
function allowing the construction of a dictionary, indexed by the student id,
that maps to this state. As usual, there is also a function that will scrub the
file of entries that are the wrong size.

Created on Feb 24, 2013

@author: waldo
'''

#import convertfiles.xmltocsv

class coursestudentstate(object):
    '''
    A representation of the state of student work in a course
    
    This object encapsulates the work a student has done in any
    edX course, and the course state itself. 
    
    classdocs
    '''


    def __init__(self, sid, mod_type, mod_id, student_id, state, grade, created, mod,
                 max_grade, done, course_id):
        '''
        Constructor
        '''
        self.sid = sid
        self.mod_type = mod_type
        self.mod_id = mod_id
        self.student_id = student_id
        self.state = state
        self.grade = grade
        self.created = created
        self.modified = mod
        self.max_grade = max_grade
        self.done = done
        self.course_id = course_id
        
def builddict(f, ptype = ''):
    '''
    Build a dictionary, indexed by the state id, of the course state
    
    This function builds a dictionary of the student state of a course.
    Since the state is large, this also allows building a dictionary of 
    only one part of the state, determined by the ptype that is handed
    in.
    '''
    retdict = {}
    lineno = 0
    for line in f:
        lineno += 1
        if len(line) != 11:
            print 'bad row size at line ' + str(lineno)
            continue
        [sid, modt, modi, st_id, state, gr, cr, modif, mgr, done, c_id] = line
        if (ptype != '') and (modt != ptype):
            continue
        rec = coursestudentstate(sid, modt, modi, st_id, state, gr, cr, modif,
                                 mgr, done, c_id)
        retdict[sid] = rec
        
    return retdict


# def scrubcsstate(f1, f2):
#     '''
#     Clean up the state of a cvs file representation of the student state
#     
#     This function will traverse a cvs file representation of the student
#     course state, removing any entries that do not have the right number
#     of fields (which can happen because of bad or dirty input)
#     '''
#     convertfiles.xmltocsv.scrubcsv(f1, f2, 11)
            