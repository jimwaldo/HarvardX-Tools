#!/bin/tcsh

#First, get rid of files that won't be of use
rm *wiki*
rm *.xml.gpg

#Now, decrypt everything, set up separate directories for each class, move files
#to those directories, and rename to something shorter and more uniform, and then
#create a .csv file from each of the sql files
uncompAndDecrypt.sh
separateFiles.sh
foreach d (*)
    cd $d
    renameInDirectory.sh
    foreach f (*.sql)
        sqltocsv.py $f $f:r.csv
	end
    cd ..
    end

