#!/bin/tcsh

#First, get rid of files that won't be of use
killListedFiles.py
#Next, rename filenames for course that are common between HarvardX/MITx, since org id is not specified
renameCommonCourses.py

# HarvardX
mkdir HarvardX
mv HarvardX-* HarvardX

# Harvard
mkdir Harvard
mv Harvard-* Harvard/
mv HARVARD-* Harvard/

# HSPH
mkdir HSPH
mv HSPH-* HSPH/

# HarvardKennedy School
mkdir HarvardKennedySchool
mv HarvardKennedySchool-* HarvardKennedySchool/

# HarvardXPlus
mkdir HarvardXPLUS
mv HarvardXPLUS-* HarvardXPLUS/


# Move Weekly email optin list
mkdir HarvardX/CombinedCourseData
#mv harvardx-email_opt_in-* HarvardX/CombinedCourseData # Prior to 2016-09-05, this was the naming convetion
mv HarvardX/HarvardX-email_opt_in-* HarvardX/CombinedCourseData # New name, as of 2016-09-05

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

