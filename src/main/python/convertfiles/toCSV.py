#!/usr/bin/env python

'''Convert an XML file into CSV form, parsing the whole file

This script will parse an XML file and create a cvs file equivalent.
The script takes as arguments the input file, the output file, and 
a flag to indicate whether to try whole-file parsing (if the 'w' 
flag is passed) or incremental parsing (if the 'i' flag is passed). 
Whole-file parsing produces better output, but is also more prone to
failure if the input is not perfect. Incremental parsing is robust,
but may produce some lines in the file that will be problematic for
future work; after doing an incremental parse it is probably wise
to scrub the file.

'''
import xmltocsv
import sys

if len(sys.argv) < 3:
    print 'usage: toCSV xmlFile csvFile [i,w]'
    print 'where i indicates incremental parsing'
    print 'and w indicates whole-file parsing'

if sys.argv[3] == 'i':
    xmltocsv.xmltocsviter(sys.argv[1], sys.argv[2])
elif sys.argv[3] == 'w':
    xmltocsv.xmltocsvfull(sys.argv[1], sys.argv[2])
else :
    print 'invalid mode; please indicate i (iterative) or w (whole file)'