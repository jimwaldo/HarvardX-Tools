#!/nfs/projects/c/ci3_jwaldo/MONGO/bin/python
"""
This is generic CSV to JSON converter containing newline delimited formatting

Input is a comma delimited CSV file
Output is a newline delimited JSON formatted

Usage:
python convertCSVtoJSON [-options]

OPTIONS:
--input Name of input filename
--output Name of output filename
--gzip Gzip output json file
--schema Specify JSON Schema (Optional)
--schema-name Specify JSON Schema name within json file, if it exists

class functions:
def cleanJSONline(self, d, schema_dict): # Main Clean
def applySchemaFormat(self, value, specified_type):
def checkIllegalKeys(self, d, fixkeys=True):
def readSchema(self, schema_file=None, schema_name=None):
def writeJSONline(self, x, fileHandler, schema_dict):
def writeOutJSONfile(self, writeData, outputfilename, gzipOutput, schema_file=None, schema_name=None):
def printOtherStats(self):
def calculateOverallSummary(self):
def calculateSchemaStats(self):
def printSchemaStats(self):
def printSchemaStatsPerRow(self, row):

@author: G.Lopez
"""

import os
import sys
import csv
import json
import gzip
from collections import OrderedDict
from path import path
import argparse
import pandas as pd
import re
import copy
import ast


# List of supported file types
ZIP_EXT = '.gz'
SUPPORTED_FILE_EXT = ['.csv', '.csv.gz']

# BigQuery to Python Type
BQ2PTYPE = {'RECORD': dict, 'INTEGER': int, 'STRING': unicode, 'FLOAT': float, 
            'BOOLEAN': int,
            'TIMESTAMP': unicode,
           }
TYPE_RECORD = 'RECORD'

# Define Schema Stats
SCHMA_SUMMARY_COLS = ['Correct', 'Incorrect', 'Fixed', 'Not Fixed', '% Incorrect', '% Corrected']

SCHMA_KEY_IGNORE = {'i4x-': re.compile('^i4x.*'),
		    'input_i4x': re.compile('^input_i4x.*'),
		    'submission': re.compile('{"submission":.*'),
		    'options_selected': re.compile('{"options_selected":.*')
		   }

# Replace illegal characters in key field names
# These characters are not accepted as BigQuery table field names and need to be fixed
DASH = '-'
PERIOD = '.'
REPLACE = {DASH: '_',
           PERIOD: '__'
          }

class convertCSVtoJSON(object):

	def __init__(self):

		# Initialize options to None
		self.writeData = None
		self.outputfilename = None
		self.gzipOutput = None
		self.schema_file = None
		self.schema_name = None

		# Maintain Intermediate Stats / Counting
		self.LINE_CNT = 0
		self.LINE_CNT_1000 = 1000
		self.NONE_CNT_DICT = {}	 # Empty Fields Count
		self.VALUE_CNT_DICT = {}	 # Non-Empty Fields Count
		self.SCHMA_OK_CNT_DICT = {}   # Schema matches field format
		self.SCHMA_NOK_CNT_DICT = {}  # Schema doesn't match field format
		self.SCHMA_CVT_CNT_DICT = {}  # Non-matching field converted to Schema Format
		self.SCHMA_NCVT_CNT_DICT = {}  # Non-matching field could NOT be converted to Schema Format
		self.SCHMA_BAD_KEY = {}        # Bad/Unknown Keys
		self.SCHMA_FIXED_KEYS = {}     # Fixed Keys
		self.SCHMA_IGNORE_KEYS = {}    # Ignored Keys
		self.SCHMA_IGNORE_KEY_EXIST = {} # Ignored Key per Regular Expression
		self.SCHMA_SUMMARY = pd.DataFrame( columns=SCHMA_SUMMARY_COLS  )

		# Maintain Overall stats	
		self.total_pop_fields = 0
		self.total_pop_fields_correct = 0
		self.total_pop_fields_incorrect = 0
		self.total_pop_fields_corrected = 0
		self.total_pop_fields_notcorrected = 0
		self.total_pop_fields_bad = 0
		self.total_pop_fields_ignore = 0
		self.pct_correct = 0
		self.pct_incorrect = 0
		self.pct_incorrect_fixed = 0
		self.pct_incorrect_notfixed = 0
		self.pct_bad_unknown = 0
		self.pct_ignored_keys = 0 

	def cleanJSONline(self, d, schema_dict, applySchema=True):
		"""
		First, Delete keys with the value ``None`` in a dictionary, recursively.
		Second, Check Schema for keys that exist, if schema dictionary is specified
		"""

		# d.iteritems isn't used as you can't del or the iterator breaks.
		for key, value in d.items():

			if type(value) is unicode:
				try:	
					value = ast.literal_eval(value)
				except:	
					pass

			if type(key) is unicode:
				try:	
					key = ast.literal_eval(key)
				except:	
					pass
				
			if value is None:
				del d[key]

				# Record for stats
				self.__addNoneDict__(key)

			elif isinstance(value, dict):

				try:
					if key in schema_dict:
						
						# Pass dictionary value recursively until root is found
						self.cleanJSONline(value, schema_dict[key], applySchema=applySchema)
						
						# Record value for stats
						self.__addValueDict__(key)
					else:
						# Value is a dictionary, but key is not, so root found and schema should be checked
						self.checkSchemaFormat(key, value, schema_dict, applySchema=applySchema)

						# Record value for stats
						self.__addValueDict__(key)
				except:
					print "eerror: value=%s, key=%s, schema=%s" % (value, key, schema_dict)
					raise
					continue

			# Root found
			else:
		
				# Record stats for populated field
				self.__addValueDict__(key)

				# If schema is specified, then attempt to convert incorrect fields into correct format
				if schema_dict is not None: 

					new_value = self.checkSchemaFormat(key, value, schema_dict, applySchema=applySchema)
				
					# Apply schema and assign to existing value, if specified
					if new_value is not None:
						d[key] = new_value
		return d

	def checkSchemaFormat(self, key, value, schema_dict, applySchema):
		"""
		Check schema format according to schema dictionary, if provided, then optionally correct
		"""

		if key in schema_dict:

			try:
				specified_type = BQ2PTYPE[schema_dict[key]]
			except:
				specified_type = schema_dict

		# Key does not exist in defined schema 
		else:

			self.__addBadIgnoreKeys__(key)
			return

		# Mismatch identified
		if type(value) in [float, int, unicode] and type(value) != specified_type:

			# Record stats for populated field with incorrect format
			self.__addValueNotOkDict__(key)

			# Attempt to convert incorrect fields according to specified schema
			if applySchema:
				try:
					new_value = self.applySchemaFormat(value, specified_type)
					# Record stats for populated field wit incorrect format and successfully converted field
					self.__addConvertedDict__(key)
					return new_value
					
				except:

					# Record stats for populated field wit incorrect format and unconverted field
					self.__addNotConvertedDict__(key)

					return

		# Schema and current field format matches
		else:

			self.__addValueOkDict__(key)

		return

	def __addConvertedDict__(self, key):
		"""
		Add provided key to the Converted success dict, for summary stats
		"""
		if key not in self.SCHMA_CVT_CNT_DICT:
			self.SCHMA_CVT_CNT_DICT[key] = 1
		else:
			self.SCHMA_CVT_CNT_DICT[key] += 1

	def __addNotConvertedDict__(self, key):
		"""
		Add provided key to the Conversion failure dict, for summary stats
		"""
		if key not in self.SCHMA_NCVT_CNT_DICT:
			self.SCHMA_NCVT_CNT_DICT[key] = 1
		else:
			self.SCHMA_NCVT_CNT_DICT[key] += 1

	def __addValueOkDict__(self, key):
		"""
		Add provided key to the Value Schema OK dict, for summary stats
		"""
		if key not in self.SCHMA_OK_CNT_DICT:
			self.SCHMA_OK_CNT_DICT[key] = 1
		else:
			self.SCHMA_OK_CNT_DICT[key] += 1

	def __addValueNotOkDict__(self, key):
		"""
		Add provided key to the Value Schema mismatch dict, for summary stats
		"""
		if key not in self.SCHMA_NOK_CNT_DICT:
			self.SCHMA_NOK_CNT_DICT[key] = 1
		else:
			self.SCHMA_NOK_CNT_DICT[key] += 1

	def __addValueDict__(self, key):
		"""
		Add provided key to the populated value dictionary, for summary stats
		"""

		# Record stats for populated field
		if key not in self.VALUE_CNT_DICT:
			self.VALUE_CNT_DICT[key] = 1
		else:
			self.VALUE_CNT_DICT[key] += 1

	def __addNoneDict__(self, key):
		"""
		Add provided key to None Dictionary for summary statistics
		"""

		# Record for stats
		if key not in self.NONE_CNT_DICT:
			self.NONE_CNT_DICT[key] = 1            
		else:
			self.NONE_CNT_DICT[key] += 1

	def __addBadIgnoreKeys__(self, key):
		"""
		Determine if provided key should be ignored based on ignore dictionary
		"""
		keyIgnored = False
		# Check if this is a key to Ignore
		for ignore_key in SCHMA_KEY_IGNORE:
			m = SCHMA_KEY_IGNORE[ignore_key].match(key)

			# This is a key to ignore
			if m:
				#print "key %s ignored" % key
				keyIgnored = True
				# Record count for each type of reg exp ignored
				if ignore_key not in self.SCHMA_IGNORE_KEY_EXIST:
					self.SCHMA_IGNORE_KEY_EXIST[ignore_key] = 1
				else:
					self.SCHMA_IGNORE_KEY_EXIST[ignore_key] += 1

				# Record count for each unique ignored key
				if key not in self.SCHMA_IGNORE_KEYS:
					self.SCHMA_IGNORE_KEYS[key] = 1
				else:
					self.SCHMA_IGNORE_KEYS[key] += 1
				break

		# If this is a key NOT to ignore, then this is a bad key
		if not keyIgnored:
			#print "bad key %s " % key

			if key not in self.SCHMA_BAD_KEY:
				self.SCHMA_BAD_KEY[key] = 1
			else:
				self.SCHMA_BAD_KEY[key] += 1

		return keyIgnored

	def applySchemaFormat(self, value, specified_type):
		"""
		This function will compare the current key value field to the specified format schema for this field
		and then an attempt to convert will be performed. If successful, return value and assign it. Otherwise,
		raise an error
		"""
		new_value = None
		if type(value) is float and specified_type is int:

			try:
				new_value = int(value) 
			except:
				raise

		elif type(value) is int and specified_type is float:

			try:
				new_value = float(value)
			except:
				raise

		elif type(value) is unicode and specified_type is int:
			try:
				new_value = int(float(value.encode("ascii")))
			except:
				pass
				try:
					new_value = int(value.encode("ascii"))
				except:
					raise

		elif type(value) is unicode and specified_type is float:
			try:
				new_value = float(value.encode("ascii"))
			except:
				raise

		elif (type(value) is float or type(value) is int) and specified_type is unicode:
			try:
				new_value = str(value)
			
			except:
				raise
		else:
			print "[applySchemaFormat]: Format not handled: value %s, spec_type %s" % (type(value), specified_type)
			raise

		return new_value

	def checkIllegalKeys(self, d, fixkeys=True):
		"""
		This function will check for illegal keys according to the REPLACE dictionary.
		Optionally, fix the keys according to the dictionary to prevent illegal keys when importing into BigQuery
		"""
		illegal_keys_exist = False

		# Lastly, check for illegal characters in keys and replace
		for key, value in d.items():
			if DASH in key or PERIOD in key:
				illegal_keys_exist = True
				illegal_key = key
				new_key = key.replace(DASH, REPLACE[DASH]).replace(PERIOD, REPLACE[PERIOD])
				if illegal_key not in self.SCHMA_BAD_KEY:
					self.SCHMA_BAD_KEY[illegal_key] = new_key
				if new_key not in self.SCHMA_FIXED_KEYS:
					self.SCHMA_FIXED_KEYS[new_key] = 1
				else:
					self.SCHMA_FIXED_KEYS[new_key] += 1

		if illegal_keys_exist and fixkeys:
			# Need to rebuild ordered dict
			goodkeys = OrderedDict((self.SCHMA_BAD_KEY[k] if k in self.SCHMA_BAD_KEY else k, v) for k, v in d.iteritems())
			return goodkeys
		else:
			return d
			    
	def readSchema(self, schema_file=None, schema_name=None):
		"""	
		Function will read the specified schema and will be used for comparing each json key/value pair
		"""
		if schema_name is None:
			schema = json.loads(open(schema_file).read())
		else:
			schema = json.loads(open(schema_file).read())[schema_name]

		def schemaDict(input_schema):
			schema_dict = OrderedDict()
			schema = copy.deepcopy(input_schema)
			for keys in schema:
				schema_dict[keys.get('name', None)] = keys.get('type', None)
				if keys['type'] == TYPE_RECORD:
					#schema_dict['dict_schema'] = schemaDict(keys['fields'])
					schema_dict[keys.get('name', None)] = schemaDict(keys['fields'])
			return schema_dict
		schema_dict = schemaDict(schema)

		print "--------------------------------"
		print "SCHEMA SPECIFIED"
		print "--------------------------------"
		print(json.dumps(schema_dict, indent=4))

		return schema_dict


	def writeJSONline(self, x, fileHandler, schema_dict):
		"""
		Write out single newline delimited JSON line output, while maintaining column ordering
		"""

		try:
			# Process rows and writ out
			rec = x.to_json(orient="index", force_ascii=True)
			rec_json = json.loads(rec, object_pairs_hook=OrderedDict)
			rec_json_cleaned = self.cleanJSONline(rec_json, schema_dict)
			rec_json_cleaned_verified_keys = self.checkIllegalKeys(rec_json_cleaned)
			fileHandler.write(json.dumps(rec_json_cleaned_verified_keys) + "\n")

			# Print procesing Counter
			self.LINE_CNT = self.LINE_CNT + 1
			if self.LINE_CNT % self.LINE_CNT_1000 == 0:
				sys.stdout.write("[main]: %dk Lines processed\r" % (self.LINE_CNT / self.LINE_CNT_1000 ) )
				sys.stdout.flush()
		except:
			print "[main]: Error writing json line %s\n" % rec
			raise
			pass 

	def writeOutJSONfile(self, writeData, outputfilename, gzipOutput, schema_file=None, schema_name=None):
		"""
		Create JSON file based on options for --output and --gzip
		""" 
		if gzipOutput:
			ofp = gzip.GzipFile(outputfilename, 'w')
		else:
			ofp = open(outputfilename, 'w')

		schema_dict = None
		if schema_file is not None:
			schema_dict = self.readSchema(path(schema_file), schema_name)

		writeData.apply(self.writeJSONline, args=[ofp, schema_dict], axis=1)
	    
		(self.rows, self.cols) = writeData.shape
		self.outputfilename = outputfilename

	def printOtherStats(self):
		"""
		Print missing field and value statistics
		"""
		print "--------------------------------"
		print "MISSING FIELDS SUMMARY"
		print "--------------------------------"
		if self.NONE_CNT_DICT:
			for field in sorted(self.NONE_CNT_DICT, key=self.NONE_CNT_DICT.get, reverse=True):
				print "[main]: Field name: %s, None/Null count: %s" % (field, self.NONE_CNT_DICT[field])
		
		print "--------------------------------"
		print "VALUE FIELDS SUMMARY"
		print "--------------------------------"
		if self.VALUE_CNT_DICT:
			for field in sorted(self.VALUE_CNT_DICT, key=self.VALUE_CNT_DICT.get, reverse=True):

				# Do not print Ignore Keys (there will be lots)
				if field not in self.SCHMA_IGNORE_KEYS:
					print "[main]: Field name: %s, Value count: %s" % (field, self.VALUE_CNT_DICT[field])

	def printOverallSummary(self):
		"""
		Print Overall Summary including % correct vs. incorrect. Of those incorrect, what % was fixed and not fixed
		"""

		print "--------------------------------"
		print "SUMMARY"
		print "--------------------------------"
		if self.outputfilename is not None and self.rows is not None and self.cols is not None:
			print "[main]: Finished writing JSON file %s with %s rows and %s fields max" % (self.outputfilename, self.rows, self.cols)

		print "[main]: Total Populated Fields = %s" % self.total_pop_fields
		print "[main]: Total Populated Fields Correct = %s" % self.total_pop_fields_correct
		print "[main]: Total Populated Fields Incorrect = %s" % self.total_pop_fields_incorrect
		print "[main]: Total Populated Fields Corrected = %s" % self.total_pop_fields_corrected
		print "[main]: Total Populated Fields Not Corrected = %s" % self.total_pop_fields_notcorrected
		print "[main]: Total Populated Bad/Unknown Fields = %s" % self.total_pop_fields_bad
		print "[main]: Total Populated Ignored Fields = %s" % self.total_pop_fields_ignore

		print "[main]: Pct Correct = %0.3f%%" % self.pct_correct
		print "[main]: Pct InCorrect = %0.3f%%" % self.pct_incorrect
		print "[main]: Pct InCorrect Fixed = %0.3f%%" % self.pct_incorrect_fixed
		print "[main]: Pct InCorrect Not Fixed= %0.3f%%" % self.pct_incorrect_notfixed
		print "[main]: Pct Bad/Unknown Fields Not Fixed = %0.3f%%" % self.pct_bad_unknown
		print "[main]: Pct Ignored Fields = %0.3f%%" % self.pct_ignored_keys

	def calculateOverallSummary(self):
		"""
		Function to calculate Overall Stats
		"""

		self.pct_correct = float(float(self.total_pop_fields_correct) / float(self.total_pop_fields)) * 100.00 if self.total_pop_fields != 0 else 0.0
		self.pct_incorrect = float(float( self.total_pop_fields_incorrect) / float(self.total_pop_fields)) * 100.00 if self.total_pop_fields != 0 else 0.0
		self.pct_incorrect_fixed = float( float(self.total_pop_fields_corrected) / float(self.total_pop_fields_incorrect) ) * 100.00 if self.total_pop_fields_incorrect != 0 else 0.0
		self.pct_incorrect_notfixed = float( float(self.total_pop_fields_notcorrected) / float(self.total_pop_fields_incorrect) ) * 100.00 if self.total_pop_fields_incorrect != 0 else 0.0
		self.pct_bad_unknown = float( float(self.total_pop_fields_bad) / float(self.total_pop_fields) ) * 100.00 if self.total_pop_fields != 0 else 0.0
		self.pct_ignored_keys = float(float(self.total_pop_fields_ignore) / float(self.total_pop_fields) ) * 100.00 if self.total_pop_fields != 0 else 0.0

	def calculateSchemaStats(self):
		"""
		Function to calculate Schema Stats
		"""

		if self.VALUE_CNT_DICT:
			for field in sorted(self.VALUE_CNT_DICT, key=self.VALUE_CNT_DICT.get, reverse=True):

				# Get Populated field counts from dictionaries
				total_pop_fields = self.VALUE_CNT_DICT.get(field, 0) 	           # VALUE_CNT_DICT[field]
				total_pop_fields_correct = self.SCHMA_OK_CNT_DICT.get(field, 0)         # SCHMA_OK_CNT_DICT[field]
				total_pop_fields_incorrect = self.SCHMA_NOK_CNT_DICT.get(field, 0)      # SCHMA_NOK_CNT_DICT[field]
				total_pop_fields_corrected = self.SCHMA_CVT_CNT_DICT.get(field, 0)      # SCHMA_CVT_CNT_DICT[field]
				total_pop_fields_notcorrected = self.SCHMA_NCVT_CNT_DICT.get(field, 0)  # SCHMA_NCVT_CNT_DICT[field]

				# If not in Ignore Field Dictory and not in Bad key Dict, then calc stats
				if field not in self.SCHMA_IGNORE_KEYS and field not in self.SCHMA_BAD_KEY:


					pct_correct = float(float(total_pop_fields_correct) / float(total_pop_fields)) * 100.00 if total_pop_fields != 0 else 0.0
					pct_incorrect = float(float( total_pop_fields_incorrect) / float(total_pop_fields)) * 100.00 if total_pop_fields != 0 else 0.0
					pct_incorrect_fixed = float( float(total_pop_fields_corrected) / float(total_pop_fields_incorrect) ) * 100.00 if total_pop_fields_incorrect != 0 else 0.0
					pct_incorrect_notfixed = float( float(total_pop_fields_notcorrected) / float(total_pop_fields_incorrect) ) * 100.00 if total_pop_fields_incorrect != 0 else 0.0
					self.SCHMA_SUMMARY.ix[field, 'Field'] = field
					self.SCHMA_SUMMARY.ix[field, 'Correct'] = total_pop_fields_correct
					self.SCHMA_SUMMARY.ix[field, 'Incorrect'] = total_pop_fields_incorrect
					self.SCHMA_SUMMARY.ix[field, 'Fixed'] = total_pop_fields_corrected
					self.SCHMA_SUMMARY.ix[field, 'Not Fixed'] = total_pop_fields_notcorrected
					self.SCHMA_SUMMARY.ix[field, '% Incorrect'] = pct_incorrect
					self.SCHMA_SUMMARY.ix[field, '% Corrected'] = pct_incorrect_fixed

				# Maintain overall count
				self.total_pop_fields = self.total_pop_fields + total_pop_fields
				self.total_pop_fields_correct = self.total_pop_fields_correct + total_pop_fields_correct
				self.total_pop_fields_incorrect = self.total_pop_fields_incorrect + total_pop_fields_incorrect
				self.total_pop_fields_corrected = self.total_pop_fields_corrected + total_pop_fields_corrected
				self.total_pop_fields_notcorrected = self.total_pop_fields_notcorrected + total_pop_fields_notcorrected

	def printSchemaStats(self):
		"""
		Function to print Schema Stats
		"""

		# Print stats for schema verification
		print "--------------------------------"
		print "SCHEMA CHECK SUMMARY"
		print "--------------------------------"

		# Sort by % not fixed to identify problem areas
		self.SCHMA_SUMMARY.sort(['% Incorrect'], inplace=True, ascending=False)
		self.SCHMA_SUMMARY.apply(self.printSchemaStatsPerRow, axis=1)

		# Print Bad Keys, if they exist
		if self.SCHMA_BAD_KEY:
			for field in self.SCHMA_BAD_KEY:
				if type(self.SCHMA_BAD_KEY[field]) is int:

					print "[main]: Bad/Unknown Field name: %s, %s values ignored since does not exist in schema" % (field, self.SCHMA_BAD_KEY[field])
					self.total_pop_fields_bad = self.total_pop_fields_bad + self.SCHMA_BAD_KEY[field]

				if type(self.SCHMA_BAD_KEY[field]) is unicode:

					print "[main]: Bad/Unknown Field name: %s replaced with %s (Fixed %s occurrences)" % (field, self.SCHMA_BAD_KEY[field], self.SCHMA_FIXED_KEYS[self.SCHMA_BAD_KEY[field]])
					self.total_pop_fields_bad = self.total_pop_fields_bad + self.SCHMA_BAD_KEY[field]
		
		if self.SCHMA_IGNORE_KEY_EXIST:
			for ignore_key in self.SCHMA_IGNORE_KEY_EXIST:
				print "[main]: Ignored fields that match regex %s, (%s occurrences)" % (SCHMA_KEY_IGNORE[ignore_key].pattern, self.SCHMA_IGNORE_KEY_EXIST[ignore_key] )
				self.total_pop_fields_ignore = self.total_pop_fields_ignore + self.SCHMA_IGNORE_KEY_EXIST[ignore_key]
		

	def printSchemaStatsPerRow(self, row):
		"""
		Help function to print stats for each field
		"""
	    
		print "[main]: Known Field name: %s, Correct: %s, Incorrect: %s, Fixed: %s, Not Fixed: %s (%0.2f%% incorrect, %0.2f%% corrected)" % ( row['Field'], row['Correct'], row['Incorrect'], row['Fixed'], row['Not Fixed'], row['% Incorrect'], row['% Corrected'] )


def main():
	"""
	Main Convert CSV to JSON program 
	""" 
	global NONE_CNT_DICT, VALUE_CNT_DICT

	# Setup Command Line Options
	text_help = '''usage: %prog [-options] '''
	text_description = ''' Convert CSV to JSON script '''
	parser = argparse.ArgumentParser( prog='PROG',
				  description=text_description)
	parser.add_argument("--input", type=str, help="Name of input file", required=True)
	parser.add_argument("--output", type=str, help="Name of output file", required=True)
	parser.add_argument("--gzip", help="Gzip output file", action="store_true")
	parser.add_argument("--schema", type=str, help="Specify JSON Schema")
	parser.add_argument("--schema-name", type=str, help="Specify JSON Schema Name")
	args = vars(parser.parse_args())
	print "[main]: arguments passed => %s" % args

	# Read Input File
	print "[main]: Reading CSV input file %s " % args['input']
	try:
		if os.path.exists(args['input']):
			for ext in SUPPORTED_FILE_EXT:
				if ext in args['input'] and args['input'].endswith(ZIP_EXT):
					inputData = pd.read_csv(gzip.GzipFile(args['input']), sep=",")
					break
				elif ext in args['input']:
					inputData = pd.read_csv(args['input'], sep=",")
					break
				else:
					print "[main]: File type not supported"
					exit()
		else:
			print "[main]: File does not exist"
			exit()
	except:
		print "[main]: Error reading file"
		raise

	# Convert to JSON
	try:
		# Process Input
		converter = convertCSVtoJSON()
		converter.writeOutJSONfile(inputData, args['output'], args['gzip'], args['schema'], args['schema_name'] )

		# Print stats for missing/null data, Print stats for populated data
		converter.printOtherStats()
		converter.calculateSchemaStats()
		converter.printSchemaStats()

		# Print Final Summary
		converter.calculateOverallSummary()
		converter.printOverallSummary()
	except:
		print "[main]: ERROR => Failed to write JSON output"
		raise

if __name__ == '__main__':
	main()
