#!/usr/bin/env python
"""
Test Script that checks the existence of time hacks within 2 log files as input.
Optionally, specifying "-o" as an option will create a delta log file containing all the missing time hacks
This script assumes that one of the log files contains a subset of time hacks of the other log file
"""
import sys
import json 
from dateutil import parser
import time


def compareLogs(logOne, logTwo, outTimes=False):

	mismatches = 0
	dateDict = {}
	diffCreated = False
	for d in sorted(logOne, key=logOne.get, reverse=True):
		for l in logOne[d]:
			
			try:
				if l in logTwo[d]:
					logThis = "Time %s exists in first, but not second" % (d)

			except KeyError:
				mismatches += 1
				
				# Find out what days
				currentTime = parser.parse(d)
				currentDate = currentTime.date()
				ctime = currentTime.time()
				if currentDate not in dateDict:
					dateDict[currentDate] = 1
				else:
					dateDict[currentDate] += 1
				
				logThis = "Missing Time Hack (only exists in one log file): %s" % (d)
				logger(logThis)

				# outTimes is true, then output to file
				if outTimes:
					if not diffCreated:
						diffCreated = True
						fname = time.strftime("testSameEvents_%m_%d_%Y-%H_%M_%S_timelist.txt")
						diffFile = open(fname, 'w')

					diffFile.write(d + "\n")
	
	return mismatches, dateDict

def logger(logit):
	
	global logCreated
	global logFile

	if not logCreated:	
		logCreated = True
		fname = time.strftime("testSameEvents_%m_%d_%Y-%H_%M_%S.txt")
		print "creating file: ", fname
		logFile = open(fname, 'w')

	logFile.write(logit + "\n")

def openAndRead(fname):

	lineDictForLog = {}
	lineNo = 1
	fout = open(fname, 'r')
	for line in fout:
		try:
			dcl = json.loads(line)
			ts = dcl['time']
			if ts not in lineDictForLog:
				lineDictForLog[ts] = [line]
			else:
				lineDictForLog[ts].append(line)
			lineNo += 1
		except ValueError:
			print "[Error]: Could not find time"
			
	fout.close()
	return lineDictForLog


if __name__ == '__main__':


	global logCreated
	global logFile
	logCreated = False
	logFile = 0

	# Takes 2 files as input (3rd optional for outputfile)
	fileOne = sys.argv[1]		
	fileTwo = sys.argv[2]
	timeDiffs = len(sys.argv) >= 4 and sys.argv[3] == '-o'

	logMsg1 = "LogOne File = %s" % (fileOne)
	logMsg2 = "LogTwo File = %s" % (fileTwo)
	logger(logMsg1)
	logger(logMsg2)

	logOneDict = {}
	logTwoDict = {}

	logOneDict = openAndRead(fileOne)
	logTwoDict = openAndRead(fileTwo)
	
	dailyLogMismatchOne = {}
	dailyLogMismatchTwo = {}
	
	mismatches = 0
	mismatches_logOneLogTwo = 0
	mismatches_logTwoLogOne = 0

	# Check if fileOne events exist in fileTwo events
	mismatches_logOneLogTwo, dailyLogMismatchTwo  = compareLogs(logOneDict, logTwoDict, timeDiffs)
	mismatches_logTwoLogOne, dailyLogMismatchOne  = compareLogs(logTwoDict, logOneDict, timeDiffs)
	
	logMsg3 = "Total Mismatches (LogOne vs. LogTwo): %s" % mismatches_logOneLogTwo 
	logMsg4 = "Total Mismatches (LogTwo vs. LogOne): %s" % mismatches_logTwoLogOne 
	logMsg5 = "# of Mismatches per Day"
	print logMsg3
	print logMsg4
	print logMsg5
	logger(logMsg1)
	logger(logMsg2)
	logger(logMsg3)
	logger(logMsg4)
	logger(logMsg5)
	for o in iter(dailyLogMismatchOne):
		msg = "Daily Log: %s, Count: %s" % ( o, dailyLogMismatchOne[o] )
		print msg
		logger(msg)
	for t in iter(dailyLogMismatchTwo):
		msg = "Daily Log: %s, Count: %s" % ( t, dailyLogMismatchTwo[t] )
		print msg
		logger(msg)

