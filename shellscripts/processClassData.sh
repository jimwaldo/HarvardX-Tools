#!/bin/tcsh

#First, get rid of files that won't be of use
killListedFiles.py
mkdir HarvardX
mv HarvardX-* HarvardX
mkdir Harvard
mv Harvard-* Harvard/
mv HARVARD-* Harvard/
mkdir HSPH
mv HSPH-* HSPH/
mkdir HKS
mv HarvardKennedy* HKS/

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

