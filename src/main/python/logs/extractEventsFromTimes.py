#!/usr/bin/env python
'''
 Given a list of times, extract log events from input log

'''
import json
import sys

if __name__ == '__main__':

	if len(sys.argv) < 4:
		print "[Error] Too Few Arguments:"
		print "Usage: extractEventsFromTimes.py logFile timeList outputfile"
		exit()

	logFile = sys.argv[1]	
	timeList = sys.argv[2]
	outputFile = sys.argv[3]
	timeSlices = {}

	# Go through list of times	
	fout_timeList = open(timeList, 'r')
	for line in fout_timeList:
		line = str(line.rstrip('\n'))
		if line not in timeSlices:
			timeSlices[line] = 1
		else:
			timeSlices[line] += 1
	print "length %s " % len(timeSlices)

	# Open new file to write 	
	fout_outFile = open(outputFile, 'w')
	
	# Go through log file
	fout_logFile = open(logFile, 'r')
	lineCnt = 0
	for line in fout_logFile:
		try:
			dcl = json.loads(line)
			ts = dcl['time']
			ts = str(ts)
			if ts in timeSlices:
				lineCnt += 1
				fout_outFile.write(line)
		except:
			pass

	print "Found %s time deltas" % lineCnt
	fout_outFile.close()
				

