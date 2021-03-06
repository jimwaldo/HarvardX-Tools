#!/usr/bin/env python

"""
Find all of the event types in a JSON-style log dump that originated in the browser.

This script will take as input an edX activity log file and find all
of the event types in that file. The resulting event types will be
written to a file, one type per line, and the number of event types
(which may be very large) will be displayed at the end of the
run. The script will deal with non-ascii characters, writing the
output file as a latin-1 encoding

"""
import json
import sys
import codecs

if __name__ == '__main__':
    infile = open(sys.argv[1], 'r')
    outfile = codecs.open(sys.argv[2], 'w', 'latin-1', 'replace')
    typelist = set()
    i = 0
    for line in infile:
        elems = json.loads(line)
        etype = elems['event_type']
        if (elems['event_source'] == 'browser'):
            if etype not in typelist:
                typelist.add(etype)
                outfile.write(etype + '\n')
                i = i + 1
    
    print 'Total number of event types : ', i



        

