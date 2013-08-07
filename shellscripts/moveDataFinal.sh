#!/bin/tcsh
# When run in the directory containing the week's dump of edX research data as
# produced by processClassData.sh and processLogData.sh, will move the files to
# the directory setup that has been decided on for the IQSS servers. In particular,
# a directory for the week's data will be created under a directory for each class,
# and all of the data for the week will be moved to that directory. In addition, if
# there is a non-empty weekly log, that log will be moved and added to the end of
# the full log for the course

moveWeeklyToClass.py $1 $2 $3

cd $1
foreach d ([C-U]*)
    cd $d
    if -e $2/WeekLog then
        if -z $2/WeekLog then 
            rm $2/WeekLog
        else
	    cat $2/WeekLog >>Full_Log.log
    cd ..


