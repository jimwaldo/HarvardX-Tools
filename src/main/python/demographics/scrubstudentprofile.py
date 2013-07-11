#!/usr/bin/env python
'''
Scrub a csv file containing student profile records 

Removes any line in a csv file of student profile records that does
not contain the correct number of entries. Useful for cleaning up 
incremental parsing of the XML files.

Created on Feb 24, 2013

@author: waldo
'''
import userprofile
import sys

userprofile.scrubprofile(sys.argv[1], sys.argv[2])