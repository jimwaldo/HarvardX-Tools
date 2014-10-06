#!/bin/tcsh
# Process all of the log data from an edX dump. This script will result in a WeeklyLog for
# each course, in the course directory, and daily log files as a sibling of the host name
# directories and separated by organization id's.
# The script takes two parameters-- the first is the day from which the log entries are
# to be processed (the first day of the week) in YYYY-MM-DD format, while the second is 
# the identifier of the week, in YYYY-MM-DD format, generally the timestamp of the log
# file dump produced by edX (and which tends to be the last day the log files were collected
# in this dump). The start and end date will process log files with the YYYY-MM-DD format, inclusive.

#Now, uncompress the logs, and separate out the log entries in each directory by the class
uncompAndDecrypt.sh
separateClassLogs.py $1 $2

# Create WeeklyLog for each course, in their respective course directories
moveWeeklyLogs.py Harvard .
moveWeeklyLogs.py HarvardKennedySchool .
moveWeeklyLogs.py HarvardX .
moveWeeklyLogs.py HSPH .
