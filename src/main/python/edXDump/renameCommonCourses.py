#!/usr/bin/env python
"""
Identify known Harvard/MIT courses and rename files to mapped org ID

"""
from masterLookup import *
import glob
import os
import buildClassList

unknown = str("unknown")

def renameFile(flist):
    
    listOfCommonCourses = {}
    for f in flist:
       try:
           orgId = f.split('-')[0]
           cnameprefix = f.split('-')[1]
           cnameterm = f.split('-')[2]
           
           cname = str(cnameprefix) + str('-') + str(cnameterm)
           postSlice = len(f)
           preSlice = len(orgId)
           cname_fileid = f[preSlice:postSlice]

       except ValueError:
           cname = unknown
           orgId = unknown
           cnameprefix = unknown
           cnameterm = unknown
           pass
       
       if orgId in known_HarvardMIT_courses:
            
            cname_file = known_HarvardMIT_courses[orgId] + cname_fileid
            print "Renaming from %s to %s " % (f, cname_file)
            os.rename(f, cname_file)
            if cname not in listOfCommonCourses:
                listOfCommonCourses[cname] = known_HarvardMIT_courses[orgId]

    return listOfCommonCourses

if __name__ == '__main__':

    flist = glob.glob('*.*')
    common_HarvardMIT_courses = renameFile(flist)
    
    print "Common list ", common_HarvardMIT_courses
    classesToAdd = common_HarvardMIT_courses.keys()
    #buildClassList.writeList(open('weeklyClassList', 'a'), classesToAdd)


