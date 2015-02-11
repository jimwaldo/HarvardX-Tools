#!/usr/bin/env python
"""
This file grabs the latest data files, based on current date, from a specified time window, or 
grabs the latest log files from a specified start and end date. It assumes that the log filename
contains the date of that respective file.

The output is a list of files (absoulte directory path), sorted in ascending order (oldest to newest).
"""

import glob
import sys
import os
import fnmatch
import re
from dateutil import parser
from operator import itemgetter
from datetime import datetime 

LOG_FILE_EXT = ['.gz',
		'.log',
	       ]

timeWindow = {\
		'one_day_ago': 1,
		'half_week_ago': 4,
		'one_week_ago': 7,
		'two_weeks_ago': 14,
		'three_weeks_ago': 27,
		'one_month_ago': 31,
		'two_months_ago': 62,
		'three_months_ago': 93
	     }

def getFilesFromTimeWindow(verbose=False, window='one_week_ago', searchDir=os.getcwd()):
	try:
		window = str(window)
	except:
		window = 'one_week_ago'
	
	# Calculate Start and End Date based on window
	currentDay_ordinal = datetime.now().toordinal()
	weekAgo_ordinal = currentDay_ordinal - timeWindow[window]
	startFromDate = datetime.fromordinal(weekAgo_ordinal).date()
	endDate = datetime.fromordinal(currentDay_ordinal).date()
	
	if verbose:
		printLogList(finalList)
	
	return getLogFilesFromDates(False, startFromDate, endDate, searchDir)

def getLogFilesFromDates(verbose=False, start=None, end=None, searchDir=os.getcwd()):
	''' 
	Recursively walk through current directory and subdirectories, looking for files that contain
	string YYYY-MM-DD with file ext .log, that are between user specified start and end dates.
	If none specified, then process all files that it finds
	Supports both Old, Old-Modified and New Formats
	  Old format
	  i.e.: prod-edxapp*/YYYY-MM-DD_HarvardX.log (for regular server)
	  	prod-edge-edxapp*/YYYY-MM-DD_HarvardX.log (for edge server)
		Fixed directory structure
	  Old Modified format
	  i.e: prod-edge*<alphanumeric>/YYYY-MM-DD_HarvardX.log
	       prod-edge*<alphanumeric>/YYYY-MM-DD_HarvardX.log
	       Dynamic directory structure when EdX switched to Virtual Private Cloud during week of 2014-08-22
	  New Format
	  i.e.: harvardx-edge-events-YYYY-MM-DD.log (for edge server)
	  	harvardx-edx-events-YYYY-MM-DD.log (for regular server)	
	'''

	finalList = []
	finalList_tuple = []
	datesKnown = False
	if start is not None and end is not None:
		try:
			startDate = parser.parse(start)
			endDate = parser.parse(end)
			datesKnown = True
		except:
			print "[Error]: Could not parse specified date. Proper format is YYYY-MM-DD"
			return finalList
			pass

	pattern = "\d{4}-\d{2}-\d{2}"
	# Recursively look through dir
	#path = os.getcwd()
	for dirpath, dirnames, files in os.walk(searchDir):
		for f in files:
			# Check valid file extensions
			for ext in LOG_FILE_EXT:
				if f.endswith(ext):
					m = re.search(pattern, f)
					if m:
						date = m.group(0)
						dateToCompare = parser.parse(date)
						absFilePath = dirpath + str("/") + f
						if datesKnown:
							if (dateToCompare >= startDate and dateToCompare <= endDate):
								finalList_tuple.append((absFilePath,date)) # Group 0 is the matched pattern string = YYYY-MM-DD, used for sorting purposes
						else:
							finalList_tuple.append((absFilePath,date)) # Group 0 is the matched pattern string = YYYY-MM-DD, used for sorting purposes

	finalList_tuple = sorted(finalList_tuple, key=itemgetter(1)) #last item is date

	for i, j in finalList_tuple:
		finalList.append(i) #2nd item is filename

	if verbose:
		printLogList(finalList)

	return finalList

def printLogList(listOfFiles):
	for i in listOfFiles:
		print "%s" % (i)

if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		print "Usage: grabLogs.py <timewindow>"
		print "	      where <timewindow> = 'daily', 'bi-weekly', 'weekly', 'monthly' "
		print "Using Default 'weekly', since no time window specified"
		#logList = getLogFilesFromDates(True, '2014-08-01', '2014-09-10')
		logList = getLogFilesFromDates(True)
	else:
		window = str(sys.argv[1])
		print "Processing log files %s" % window
		logList = getFilesFromTimeWindow(True, window)
