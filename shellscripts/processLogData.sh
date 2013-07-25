#!/bin/tcsh

#first, we get rid of any files that have already been processed, passing in the first date of
#a log that we want to keep as the command to the scripts

foreach d (*)
    cd $d
    cullLogFiles.py $1
    cd ..
    end

#if any of the directories is empty, simply remove it
rmdir *

#Now, uncompress the logs, and separate out the log entries in each directory by the class
foreach d (prod*)
    cd $d
    uncompAndDecrypt.sh
    separateAllByClass.py $d
    cd ..
    end

#Make directories for each of the current classes, and move the logs for that class to the directory
#Get rid of any empty directories

mergeClassLogs.sh
rmdir *

#Get rid of any empty files, and any empty directories
foreach d (*)
    cd $d
    foreach f (*)
        if -z $f rm $f
	end
    cd ..
    end
    rmdir *

#go into each of the class directories, and build a full log for that week
foreach d ([A-U]*)
    cd $d
    buildWeekLog.py
    cd ..
    end


