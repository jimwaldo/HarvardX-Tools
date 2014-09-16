#!/usr/bin/env python

from __future__ import division
import json
import sys
from dateutil import parser
def getCurrentTime(line):
	
	# Format: 2014-08-10T12:50:02.849167+00:00

	try:
		dcl = json.loads(line)
		time = dcl['time']

		#datetime_format = str('%Y-%m-%dT%H:%M:%S.%f%z')
		#currentTime = datetime.datetime.strptime(time, datetime_format)
		currentTime = parser.parse(time)
		#print "time", currentTime

	except ValueError:
		print "[Error]: Could not find time"

	return currentTime

if __name__ == '__main__':

	fileToCheck = sys.argv[1]
	print fileToCheck
	jfile = open(fileToCheck, 'r')
	currentTime = 0
	prevTime = 0
	wrongTimeOrder = 0
	
	lineCnt = 0
	for line in jfile:
		
		if (lineCnt>0):		
			currentTime = getCurrentTime(line)
		else:
			currentTime = getCurrentTime(line)
			prevTime = currentTime
		if (currentTime < prevTime):
			wrongTimeOrder += 1
			#print "[Error]: Previous Event is newer than Current Event: ", prevTime, "(Previous) vs. ", currentTime, "(Current)"

		lineCnt += 1
		prevTime = currentTime

	percentUnordered = (wrongTimeOrder) / lineCnt
	print "Total Events: ", lineCnt
	print "Total Misordered Time Events: ", wrongTimeOrder, " (", percentUnordered, "% of total)"
	
	
