#!/bin/tcsh

#First, get rid of files that won't be of use
killListedFiles.py
#Next, rename filenames for course that are common between HarvardX/MITx, since org id is not specified
renameCommonCourses.py
mkdir HarvardX
mv HarvardX-* HarvardX
mkdir Harvard
mv Harvard-* Harvard/
mv HARVARD-* Harvard/
mkdir HSPH
mv HSPH-* HSPH/
mkdir HarvardKennedySchool
mv HarvardKennedySchool-* HarvardKennedySchool/

# Move Weekly email optin list
mkdir HarvardX/CombinedCourseData
mv harvardx-email_opt_in-* HarvardX/CombinedCourseData

#Now, decrypt everything, set up separate directories for each class, move files
#to those directories, and rename to something shorter and more uniform, and then
#create a .csv file from each of the sql files
foreach d (*)
    cd $d
    uncompAndDecrypt.sh
    buildClassList.py
    separateClassFiles.py
    cd ..
    end

