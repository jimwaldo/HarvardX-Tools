#!/bin/tcsh
# Process all of the log data from an edX dump. This script will result in a WeeklyLog for
# each course, in the course directory, and a Log directory as a sibling of the course
# directories that will contain the raw files.
# The script takes two parameters-- the first is the day from which the log entries are
# to be processed (the first day of the week) in YYYY-[MM-DD format, while the second is 
# the identifier of the week, in YYYY-MM-DD format, generally the timestamp of the log
# file dump produced by edX (and which tends to be the last day the log files were collected
# in this dump.

#Now, uncompress the logs, and separate out the log entries in each directory by the class
uncompAndDecrypt.sh

separateClassLogs.py $1 $2
moveWeeklyLogs.py Harvard .
moveWeeklyLogs.py HarvardKennedySchool .
moveWeeklyLogs.py HarvardX .
moveWeeklyLogs.py HSPH .

