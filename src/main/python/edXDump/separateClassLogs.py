#!/usr/bin/env python
"""
Description:
Separate log files into Course Directory Structure using log files containing YYYY-MM-DD.log in Filename as input
Runs from Top Level Directory Structure and recursively walks through subdirectories looking for input log files. 
Optionally, specify startdate and enddate (inclusive) in format YYYY-MM-DD for processing log files between certain dates only.

Input:
Log files containing YYYY-MM-DD.log in Filename as input

Output:
Output is Course Directory structure containing both Time Corrected Raw Logs and separated Time Corrected Course Logs based on fields in the log files:
Raw logs Structure
<org_id>/<host>/YYYY/YYYY-MM-DD.log (i.e.: HarvardX/courses.edx.org/2014/2014-08-20_<org_id>.log)

Course logs Structure (pre-processed for use with moveWeeklyLogs.py)
<org_id>/coursename-term.log (i.e.: HarvardX/ER22.1x-1T2014.log)
"""
import glob
import json
import sys
import os
import re
import shutil
import fnmatch
import csv
from dateutil import parser
from collections import namedtuple
from operator import itemgetter
import grabLogs
import gzip
from masterLookup import *

unknown = str("unknown")

def addName(name, dirName=None):

	if dirName is not None:
		fname = dirName + '/' + name + '.log'
	else:
		fname = name + '.log'
	print "creating file: ", fname
	fout = open(fname, 'w')
	return fout

def getField(line, field1, field2 = None):
	
	if field1 is not None and field2 is None:

		try:
			dcl = json.loads(line)
			fieldValue = dcl[field1]
			
		except ValueError:
			# Could not find field
			fieldValue = unknown
			pass

	elif field2 is not None and field2 is not None:

		try:
			dcl = json.loads(line)
			fieldValue = dcl[field1][field2]
		except ValueError:
			# Could not find field
			fieldValue = unknown
			pass

	return fieldValue

def createTopLevelDirectory(newdir):

	if not os.path.isdir(newdir):
		os.mkdir(newdir)

def parseCourseIdField(cidf):

	#print "ParseCourseIDField"
	# There are 2 formats to process
	# 1) Transparent Key Format => <dirname>/cnameprefix/cnameterm [This is pre-March 2015, when it was introduced in Hx Logs]
	# 2) Opaque Key Identifier => "course-v1:HarvardX+cnameprefix+cnameterm"
	try:
		for id_key in COURSE_ID_KEY_FORMAT:

			# Transparent Key
			m = id_key['regex'].match(cidf)
			if m and id_key['key_type'] == 'transparent':
				dirname, cnameprefix, cnameterm = cidf.split('/')
				cname = str(cnameprefix) + str('-') + str(cnameterm)
				break

			# Opaque Key
			elif m and id_key['key_type'] == 'opaque':
				course_version_prefix = m.group().replace(':','')
				course_prefix, course_version = course_version_prefix.split('-') # Might need this in the future for course versioning
				opaque_id = cidf.replace(course_version_prefix, '')
				transparent_id = opaque_id.replace('+', '/')
				dirname, cnameprefix, cnameterm = transparent_id.split('/')
				cname = str(cnameprefix) + str('-') + str(cnameterm)
				break
			else:
				cname = unknown

	except ValueError:
		cname = unknown
		pass

	return cname

def correctTimeOrder(name, dirName):
	
	lineDict = {}
	lineNo = 1
	fname = dirName + '/' + name + '.log'
	fout = open(fname, 'r')
	for line in fout:
		try:
			dcl = json.loads(line)
			ts = dcl['time']
			if ts not in lineDict:
				lineDict[ts] = [line]
			else:
				lineDict[ts].append(line)
			lineNo += 1
			#print "time at:", ts
		except ValueError:
			print "JSON error at line", str(lineNo)
	fout.close()
	return lineDict

def writeTimeCorrectedLog(name, log, dirName):

	i = 0
	print "lenth of log", len(log)
	fname = dirName + '/' + name + '.log' #Debug
	print "creating file: ", fname
	fout = open(fname, 'w')
	for d in sorted(iter(log)):
		for l in log[d]:
			i += 1
			fout.write(l)
	print "wrote", str(i), "lines to output file", fname
	fout.close()


if __name__ == '__main__':

	if len(sys.argv) > 2:
		startDate = sys.argv[1]
		endDate = sys.argv[2]
	elif len(sys.argv) > 1:
		startDate = sys.argv[1]
		endDate = sys.argv[1]
	else:
		startDate = None
		endDate = None

	#Dictionaries
	courseListingDict = {}
	filedict = {}
	hostnameDict = {}
	dirNameDict = {}
	rawlogfileDict = {}
	rawlogdirDict = {}

	logList = grabLogs.getLogFilesFromDates(True, startDate, endDate)

	for log in logList:
		
		logName = log
		print "processing logfile", logName

		if logName.endswith('.gz'):
			# Read gzipped file
			jfile = gzip.open(logName, 'r')
		else:
			# Read '.log' extension
			jfile = open(logName, 'r')

		for line in jfile:
			isUnknown = False

			# Grab Fields of interest
			courseIdField = getField(line, 'context', 'course_id')
			dirName = getField(line, 'context', 'org_id')
			hostName = getField(line, 'host')
			timeField = getField(line, 'time')
			
			# Check only known host names
			if hostName not in known_host_names:
				hostName = unknown
			
			# Check only known dirName's
			if dirName in known_HarvardMIT_courses:
				dirName = known_HarvardMIT_courses[dirName]

			if dirName not in known_org_ids:
				dirName = unknown

			# Parse Time data
			try:
				currentTime = parser.parse(timeField)
				currentDate = str(currentTime.date())
				currentYear = str(currentTime.year)
			except:
				currentDate = unknown
				currentYear = unknown
				pass

			# Parse Course Name Data
			courseName = parseCourseIdField(courseIdField)
			if courseName in killList:
				courseName = unknown
								
			# Setup raw log file dictionary tuples
			rawlogfile = namedtuple('rawlogfile', ['school', 'host', 'year', 'date','fn'])
			rawlogdir = namedtuple('rawlogdir', ['school', 'host', 'year'])

			if hostName is unknown or currentDate is unknown or courseName is unknown or dirName is unknown:
				isUnknown = True
	
			if isUnknown:

				courseName = unknown
				if courseName not in courseListingDict:
					courseListingDict[courseName] = 1
					filedict[unknown] = addName(unknown)
				else:
					courseListingDict[courseName] += 1
				
				try:
					filedict[courseName].write(line)	
				except:
					print "[Error]: Did not write to raw file %s (Course, Time or Host is unknown:  %s,%s,%s)" % (courseName, hostName, currentDate)
					pass

			else:

				# Add to Directory Structure # i.e: Harvard, HarvardX, HSPH or HarvardKennedySchool
				if dirName not in dirNameDict:
					#dirNameDict[dirName] = 1
					dirNameDict[courseName] = dirName
					createTopLevelDirectory(dirName)

				# Add to Generic Production Server Directory
				try:
					rawlogdirDict[dirName, hostName, currentYear]
				except:
					#print "Debug: Prod Server Dir does not exist. Add tuple key to dictionary (%s, %s, %s)" % (dirName, hostName, currentYear)
					schoolHost = dirName + str('/') + hostName # i.e.: Harvard/courses.edx.org
					schoolHostYear = schoolHost + str('/') + currentYear # i.e.: Harvard/courses.edx.org/2014
					rawlogdirDict[rawlogdir(school=dirName, host=hostName, year=currentYear)] = schoolHostYear # Store full directory name
					createTopLevelDirectory(schoolHost)
					createTopLevelDirectory(schoolHostYear)
					pass
					
				# Generate Raw Log Files	
				try:
					rawfilename = currentDate + str('_') + dirName
					rawlogfileDict[dirName, hostName, currentYear, currentDate, rawfilename]
				except KeyError:
					#print "Debug: Raw Log file does not exist. Add tuple key to dictionary (%s, %s, %s)" % (dirName, hostName, currentDate)
					rawlogfileDict[rawlogfile(school=dirName, host=hostName, year=currentYear, date=currentDate, fn=rawfilename)] = addName(rawfilename, rawlogdirDict[dirName,hostName,currentYear])
					print "added raw file: %s.log to dir %s" % (rawfilename, rawlogdirDict[dirName,hostName,currentYear])
					pass
					
				# Add to Course Listing Dictionary
				if courseName not in courseListingDict:
					courseListingDict[courseName] = 1
					filedict[courseName] = addName(courseName, dirName)
				else:
					courseListingDict[courseName] += 1

				# Create Course Log Files
				try:
					filedict[courseName].write(line)	
				except:
					print "[Error]: Did not write to raw file %s" % (courseName)
					pass

				#Create Production Server Log Files
				try:
					rawlogfileDict[dirName, hostName, currentYear, currentDate, rawfilename].write(line)
						
				except:
					print "[Error]: Did not write to raw file %s %s %s %s" % (dirName, hostName, currentYear, currentDate)
					pass

		jfile.close()

	# For Courses, perform Time correction and close files
	for n in iter(filedict):
		timeCorrected = {}
		print "Closing filedict[", n, "]"
		filedict[n].close()
		if n is not unknown:
			timeCorrected = correctTimeOrder(n, dirNameDict[n])
			writeTimeCorrectedLog(n, timeCorrected, dirNameDict[n])

	# For Generic Product Server Directories, perform Time correction and close files
	for g in iter(rawlogfileDict):
		timeCorrect = {}
		rawlogfileDict[g].close()
		if g.date is not unknown or g.host is not unknown:
			timeCorrected = correctTimeOrder(g.fn, rawlogdirDict[g.school, g.host, g.year])
			writeTimeCorrectedLog(g.fn, timeCorrected, rawlogdirDict[g.school, g.host, g.year])

	# Print sorted in Descending order
	for d in sorted(dirNameDict, key=dirNameDict.get, reverse=True):
		print "Directory Name: %s, Course Name: %s" % (dirNameDict[d], d)
			
	# Write Class output (descending order)
	clFile = csv.writer(open('ClassList.csv', 'w'))
	for c in sorted(courseListingDict, key=courseListingDict.get, reverse=True):
		if c is not unknown:
			print "Course Name: %s, Count: %s" % (c, courseListingDict[c])
			clFile.writerow([c, courseListingDict[c], dirNameDict[c]])	
	
	print "End of File"

