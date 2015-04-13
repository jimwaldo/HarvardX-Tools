#!/nfs/projects/c/ci3_jwaldo/MONGO/bin/python
"""
This function will check an existing JSON newline delimited file
against a specified schema

Input is a newline delimited JSON file and schema file
Output is a summary printout of statistics

Usage:
python checkJSON [-options]

OPTIONS:
--input Name of input filename (required)
--output Name of output filename
--schema Specify JSON Schema (required)
--schema-name Specify JSON Schema name within json file, if it exists

@author: G.Lopez
"""

import convertCSVtoJSON as converter
from path import path
import json
from collections import OrderedDict
import argparse
import sys
import gzip

# Maintain Stats
LINE_CNT = 0
LINE_CNT_1000 = 1000

def checkJSON(inputFile, schemaFile, schemaName=None):

	global LINE_CNT

	# Read specified schema file
	checkFormat = converter.convertCSVtoJSON()
	schema_dict = checkFormat.readSchema( path(schemaFile), schemaName )

	# Read JSON file
	if inputFile.endswith(".gz"):
		fin = gzip.open(inputFile, 'r')
	else:
		fin = open(inputFile, 'r')

	for line in fin:
		try:
			json_rec = json.loads(line, object_pairs_hook=OrderedDict)
			checkFormat.cleanJSONline(json_rec, schema_dict, applySchema=False)
			checkFormat.checkIllegalKeys(json_rec, fixkeys=False)
			
			# Print procesing Counter
			LINE_CNT = LINE_CNT + 1
			if LINE_CNT % LINE_CNT_1000 == 0:
				sys.stdout.write("[main]: %dk Lines processed\r" % ( LINE_CNT / LINE_CNT_1000 ) )
				sys.stdout.flush()
		except:
			print "[checkJSON]: Error parsing JSON line at line %s" % LINE_CNT
			pass

	checkFormat.printOtherStats()
	checkFormat.calculateSchemaStats()
	checkFormat.printSchemaStats()

	checkFormat.calculateOverallSummary()
	checkFormat.printOverallSummary()

def main():
	"""
	Main Program to Check Specified JSON file against Schema
	"""

	# Setup Command Line Options
	text_help = '''usage: %prog [-options] '''
	text_description = ''' Check JSON schema script '''
	parser = argparse.ArgumentParser( prog='PROG',
				  description=text_description)
	parser.add_argument("--input", type=str, help="Name of input file", required=True)
	parser.add_argument("--schema", type=str, help="Specify JSON Schema", required=True)
	parser.add_argument("--schema-name", type=str, help="Specify JSON Schema Name")
	args = vars(parser.parse_args())
	print "[main]: arguments passed => %s" % args

	# Read Input File
	print "[main]: Reading JSON input file %s " % args['input']
	checkJSON( args['input'], args['schema'], args['schema_name'] )

if __name__ == '__main__':
	main()
