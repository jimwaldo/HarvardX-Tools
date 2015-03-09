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

"""

import os
import sys
import csv
import json
import gzip
from collections import OrderedDict
import argparse
import pandas as pd

# Maintain Stats
LINE_CNT = 0
LINE_CNT_1000 = 1000
NONE_CNT_DICT = {}
VALUE_CNT_DICT = {}

# List of supported file types
ZIP_EXT = '.gz'
SUPPORTED_FILE_EXT = ['.csv', '.csv.gz']

def cleanJSONline(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.
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
            if key not in VALUE_CNT_DICT:
                VALUE_CNT_DICT[key] = 1
            else:
                VALUE_CNT_DICT[key] += 1
    return d

def writeJSONline(x, fileHandler):
    """
    Write out single newline delimited JSON line output, while maintaining column ordering
    """
    global LINE_CNT

    try:
        # Process rows and writ out
        rec = x.to_json(orient="index", force_ascii=True)
        rec_json = json.loads(rec, object_pairs_hook=OrderedDict)
        rec_json_cleaned = cleanJSONline(rec_json)
        fileHandler.write(json.dumps(rec_json_cleaned) + "\n")

        # Print procesing Counter
        LINE_CNT = LINE_CNT + 1
        if LINE_CNT % LINE_CNT_1000 == 0:
            sys.stdout.write("[main]: %dk Lines processed\r" % (LINE_CNT / 1000) )
            sys.stdout.flush()
    except:
        print "[main]: Error writing json line\n" % rec
        pass 

def writeOutJSONfile(writeData, outputfilename, gzipOutput):
    """
    Create JSON file based on options for --output and --gzip
    """ 
    if gzipOutput:
       ofp = gzip.GzipFile(outputfilename, 'w')
    else:
       ofp = open(outputfilename, 'w')

    writeData.apply(writeJSONline, args=[ofp], axis=1)
    
    return writeData.shape

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
        (rows, cols) = writeOutJSONfile(inputData, args['output'], args['gzip'])

        # Print stats for missing/null data
        print "--------------------------------"
        print "MISSING FIELDS SUMMARY"
        print "--------------------------------"
        if NONE_CNT_DICT:
            for field in sorted(NONE_CNT_DICT, key=NONE_CNT_DICT.get, reverse=True):
                print "[main]: Field name: %s, None/Null count: %s" % (field, NONE_CNT_DICT[field])

        print "--------------------------------"
        print "VALUE FIELDS SUMMARY"
        print "--------------------------------"
        if VALUE_CNT_DICT:
            for field in sorted(VALUE_CNT_DICT, key=VALUE_CNT_DICT.get, reverse=True):
                print "[main]: Field name: %s, Value count: %s" % (field, VALUE_CNT_DICT[field])

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
