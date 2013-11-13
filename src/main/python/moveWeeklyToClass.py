#!/usr/bin/env python 
''' 
Moves files from an existing weekly directory (the default IQSS format) 
into directories organized by course:

    i.e. harvardx-YYYY-MM-DD/{COURSE}/ --> sys.argv[1]/{COURSE}/sys.argv[2]/

Runs from an existing harvardx-YYYY-MM-DD/ weekly directory, containing 
a directory for each course. Pass the following args at command line:

    1) destination directory (containing directories for each course)
    2) name of new directory for the week of files being moved
    3) [optional] 'v' as a third argument to signal "verbose" printing 
        of progress; errors are printed either way

Created on July 16, 2013

@author: tmullaney
'''

import sys
import os
import shutil

def main():
    # check args
    if(len(sys.argv) < 3):
        print "[Error] Too few arguments"
        return -1

    dst_dir = sys.argv[1]
    new_dir_name = sys.argv[2]
    verbose = len(sys.argv) >= 4 and sys.argv[3] == 'v'
    cwd = os.getcwd()
    num_files_moved = 0

    if(verbose): print "Destination: " + sys.argv[1] + "/{COURSE}/" + sys.argv[2]

    # loop through each course's files
    src_dirs = os.listdir(cwd)
    for course_name in src_dirs:
        if(not os.path.isdir(course_name)):
            # some stray file, so skip it
            continue
        
        if(verbose): print "Moving files for " + course_name
        
        src_files = os.listdir(os.path.join(cwd, course_name))
        for course_file_name in src_files:
            src = os.path.join(cwd, course_name, course_file_name)
            dst = os.path.join(dst_dir, course_name, new_dir_name)
            
            #if there is no directory for this course, make one
            if (not os.path.isdir(os.path.join(dst_dir, course_name))):
                try:
                    os.mkdir(os.path.join(dst_dir, course_name))
                except OSError as err: pass
                
            # make new week dir if necessary
            if(not os.path.isdir(dst)): 
                try: os.mkdir(dst)
                except OSError as err: pass # display error on move

            # move file
            try:
                shutil.move(src, dst)
                num_files_moved += 1
            except IOError as err:
                print err

    if(verbose): print "Done. " + str(num_files_moved) + " files moved."

if __name__ == "__main__":
    main()