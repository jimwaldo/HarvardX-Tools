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

# Maintain Stats
LINE_CNT = 0
LINE_CNT_1000 = 1000
NONE_CNT_DICT = {}	 # Empty Fields Count
VALUE_CNT_DICT = {}	 # Non-Empty Fields Count
SCHMA_OK_CNT_DICT = {}   # Schema matches field format
SCHMA_NOK_CNT_DICT = {}  # Schema doesn't match field format
SCHMA_CVT_CNT_DICT = {}  # Non-matching field converted to Schema Format
SCHMA_NCVT_CNT_DICT = {}  # Non-matching field could NOT be converted to Schema Format
SCHMA_SUMMARY = {}
SCHMA_SUMMARY_COLS = ['Correct', 'Incorrect', 'Fixed', 'Not Fixed', '% Incorrect', '% Corrected']

# List of supported file types
ZIP_EXT = '.gz'
SUPPORTED_FILE_EXT = ['.csv', '.csv.gz']

# BigQuery to Python Type
BQ2PTYPE = {'RECORD': dict, 'INTEGER': int, 'STRING': unicode, 'FLOAT': float, 
            'BOOLEAN': int,
            'TIMESTAMP': unicode,
           }

def cleanJSONline(d, schema_dict):
    """
    First, Delete keys with the value ``None`` in a dictionary, recursively.
    Second, Check Schema for keys that exist, if schema dictionary is specified
    """
    global NONE_CNT_DICT, VALUE_CNT_DICT

    # d.iteritems isn't used as you can't del or the iterator breaks.
    for key, value in d.items():
        if value is None:
            del d[key]

            # Record for stats
            if key not in NONE_CNT_DICT:
                NONE_CNT_DICT[key] = 1            
            else:
                NONE_CNT_DICT[key] += 1

        elif isinstance(value, dict):
            cleanJSONline(value)

        else:
	
	    # Record stats for populated field
            if key not in VALUE_CNT_DICT:
                VALUE_CNT_DICT[key] = 1
            else:
                VALUE_CNT_DICT[key] += 1

	    # If schema is specified, then attempt to convert incorrect fields into correct format
	    if schema_dict is not None: 
		    if key in schema_dict.keys():
			specified_type = BQ2PTYPE[schema_dict[key]]

			# Mismatch identified
			if type(value) in [float, int] and type(value) != type(specified_type):
			
			    # Record stats for populated field with incorrect format
			    if key not in SCHMA_NOK_CNT_DICT:
				SCHMA_NOK_CNT_DICT[key] = 1
			    else:
				SCHMA_NOK_CNT_DICT[key] += 1
	      
				# Attempt to convert incorrect fields according to specified schema
				try:
					if type(value) is float and specified_type is int:
					    try:
					        d[key] = int(value) 
					    except:
						raise
					elif type(value) is int and specified_type is float:
					    try:
					        d[key] = float(value)
					    except:
						raise
					elif type(value) is unicode and specified_type is int:
					    try:
						d[key] = int(float(value.encode("ascii")))
					    except:
						pass

					    try:
						d[key] = int(value.encode("ascii"))
					    except:
						raise
					elif type(value) is unicode and specified_type is float:
					    try:
						d[key] = float(value.encode("ascii"))
					    except:
						raise
				    
				        # Record stats for populated field wit incorrect format and successfully converted field
					if key not in SCHMA_CVT_CNT_DICT:
					    SCHMA_CVT_CNT_DICT[key] = 1
					else:
					    SCHMA_CVT_CNT_DICT[key] += 1
				except:

				    # Record stats for populated field wit incorrect format and unconverted field
				    if key not in SCHMA_NCVT_CNT_DICT:
					SCHMA_NCVT_CNT_DICT[key] = 1
				    else:
					SCHMA_NCVT_CNT_DICT[key] += 1
				    continue

			# Schema and current field format matches
			else:

			    if key not in SCHMA_OK_CNT_DICT:
				SCHMA_OK_CNT_DICT[key] = 1
			    else:
				SCHMA_OK_CNT_DICT[key] += 1
                    continue
    return d

    
def readSchema(schema_file=None, schema_name=None):
    
    if schema_name is None:
        schema = json.loads(open(schema_file).read())
    else:
        schema = json.loads(open(schema_file).read())[schema_name]

    schema_dict = OrderedDict()
    for keys in schema:
        schema_dict[keys.get('name', None)] = keys.get('type', None)

    print "--------------------------------"
    print "SCHEMA SPECIFIED"
    print "--------------------------------"
    print(json.dumps(schema_dict, indent=4))

    return schema_dict


def writeJSONline(x, fileHandler, schema_dict):
    """
    Write out single newline delimited JSON line output, while maintaining column ordering
    """
    global LINE_CNT

    try:
        # Process rows and writ out
        rec = x.to_json(orient="index", force_ascii=True)
        rec_json = json.loads(rec, object_pairs_hook=OrderedDict)
        rec_json_cleaned = cleanJSONline(rec_json, schema_dict)
        fileHandler.write(json.dumps(rec_json_cleaned) + "\n")

        # Print procesing Counter
        LINE_CNT = LINE_CNT + 1
        if LINE_CNT % LINE_CNT_1000 == 0:
            sys.stdout.write("[main]: %dk Lines processed\r" % (LINE_CNT / 1000) )
            sys.stdout.flush()
    except:
	print LINE_CNT
        #print "[main]: Error writing json line\n" % rec
        pass 

def writeOutJSONfile(writeData, outputfilename, gzipOutput, schema_file=None, schema_name=None):
    """
    Create JSON file based on options for --output and --gzip
    """ 
    if gzipOutput:
       ofp = gzip.GzipFile(outputfilename, 'w')
    else:
       ofp = open(outputfilename, 'w')

    schema_dict = None
    if schema_file is not None:
       schema_dict = readSchema(path(schema_file), schema_name)

    writeData.apply(writeJSONline, args=[ofp, schema_dict], axis=1)
    
    return writeData.shape

def printStats(x):
    
    print "[main]: Field name: %s, Correct: %s, Incorrect: %s, Fixed: %s, Not Fixed: %s (%0.2f incorrect, %0.2f corrected)" % ( x['Field'], x['Correct'], x['Incorrect'], x['Fixed'], x['Not Fixed'], x['% Incorrect'], x['% Corrected'] )


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
        (rows, cols) = writeOutJSONfile(inputData, args['output'], args['gzip'], args['schema'], args['schema_name'])

        # Print stats for missing/null data
        print "--------------------------------"
        print "MISSING FIELDS SUMMARY"
        print "--------------------------------"
        if NONE_CNT_DICT:
            for field in sorted(NONE_CNT_DICT, key=NONE_CNT_DICT.get, reverse=True):
                print "[main]: Field name: %s, None/Null count: %s" % (field, NONE_CNT_DICT[field])

        # Print stats for populated data
        print "--------------------------------"
        print "VALUE FIELDS SUMMARY"
        print "--------------------------------"
        if VALUE_CNT_DICT:
            for field in sorted(VALUE_CNT_DICT, key=VALUE_CNT_DICT.get, reverse=True):
                print "[main]: Field name: %s, Value count: %s" % (field, VALUE_CNT_DICT[field])

        # Print stats for schema verification
        print "--------------------------------"
        print "SCHEMA CHECK SUMMARY"
        print "--------------------------------"
	SCHMA_SUMMARY = pd.DataFrame( columns=SCHMA_SUMMARY_COLS  )
        if VALUE_CNT_DICT:
            for field in sorted(VALUE_CNT_DICT, key=VALUE_CNT_DICT.get, reverse=True):
		total_pop_fields = VALUE_CNT_DICT.get(field, 0) 	           # VALUE_CNT_DICT[field]
		total_pop_fields_correct = SCHMA_OK_CNT_DICT.get(field, 0)         # SCHMA_OK_CNT_DICT[field]
		total_pop_fields_incorrect = SCHMA_NOK_CNT_DICT.get(field, 0)      # SCHMA_NOK_CNT_DICT[field]
		total_pop_fields_corrected = SCHMA_CVT_CNT_DICT.get(field, 0)      # SCHMA_CVT_CNT_DICT[field]
		total_pop_fields_notcorrected = SCHMA_NCVT_CNT_DICT.get(field, 0)  # SCHMA_NCVT_CNT_DICT[field]
		pct_correct = float(float(total_pop_fields_correct) / float(total_pop_fields)) * 100.00 if total_pop_fields != 0 else 0.0
		pct_incorrect = float(float( total_pop_fields_incorrect) / float(total_pop_fields)) * 100.00 if total_pop_fields != 0 else 0.0
		pct_incorrect_fixed = float( float(total_pop_fields_corrected) / float(total_pop_fields_incorrect) ) * 100.00 if total_pop_fields_incorrect != 0 else 0.0
		pct_incorrect_notfixed = float( float(total_pop_fields_notcorrected) / float(total_pop_fields_incorrect) ) * 100.00 if total_pop_fields_incorrect != 0 else 0.0
		SCHMA_SUMMARY.ix[field, 'Field'] = field
		SCHMA_SUMMARY.ix[field, 'Correct'] = total_pop_fields_correct
		SCHMA_SUMMARY.ix[field, 'Incorrect'] = total_pop_fields_incorrect
		SCHMA_SUMMARY.ix[field, 'Fixed'] = total_pop_fields_corrected
		SCHMA_SUMMARY.ix[field, 'Not Fixed'] = total_pop_fields_notcorrected
		SCHMA_SUMMARY.ix[field, '% Incorrect'] = pct_incorrect
		SCHMA_SUMMARY.ix[field, '% Corrected'] = pct_incorrect_fixed
	
	# Sort by % not fixed to identify problem areas
	SCHMA_SUMMARY.sort(['% Incorrect'], inplace=True, ascending=False)
	SCHMA_SUMMARY.apply(printStats, axis=1)

        # Print Final Summary
        print "--------------------------------"
        print "SUMMARY"
        print "--------------------------------"
        print "[main]: Finished writing JSON file %s with %s rows and %s fields max" % (args['output'], rows, cols)
    except:
        print "[main]: ERROR => Failed to write JSON output"
        raise
if __name__ == '__main__':
    main()
