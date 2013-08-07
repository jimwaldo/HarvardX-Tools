#!/bin/tcsh
# Process all of the log data from an edX dump. This script will result in a WeeklyLog for
# each course, in the course directory, and a Log directory as a sibling of the course
# directories that will contain the raw files.
# The script takes two parameters-- the first is the day from which the log entries are
# to be processed (the first day of the week) in YYYY-MM-DD format, while the second is 
# the identifier of the week, in YYYY-MM-DD format, generally the timestamp of the log
# file dump produced by edX (and which tends to be the last day the log files were collected
# in this dump.

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
    if -e WeekLog then
	if -z WeekLog then rm WeekLog
	else
	    mv WeekLog ../../$2/$d/WeekLog
    cd ..
    end

#clean up the log directories, and move the logs to their own directory with the class data
rm -r [A-U]*
cd ..
mv HarvardX $2/Logs




