#!/usr/bin/env python
"""
Converts tab-separated lines from the data dumps into a csv file. 
The program takes an sql file and the name of the csv file to 
be produced. 

Created on Apr 7, 2013

@author: waldo
"""


import sys
import csv
import os
import gzip

def convertFile(fileNameIn, fileNameOut, gzipCompress=False):

    f1 = open(fileNameIn, 'r')
    if gzipCompress:
       fileNameOut = fileNameOut + ".gz"
       f2 = gzip.GzipFile(fileNameOut, 'w') 
    else:
       f2 = open(fileNameOut, 'w')
    f3 = csv.writer(f2)
    
    for line in f1:
        f3.writerow(line[:-1].split('\t'))
    
    f1.close()
    f2.close()

def compressFile( fileToCompress ):

    cmd = "gzip %s -9" % fileToCompress
    os.system(cmd)
    
if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print ('Usage: sqltocsv.py file1 file2 gzip where')
        print ('file1 is an existing .sql file from edx and')
        print ('file2 is the name of the .csv file to produce')
        print ('gzip is whether the .csv should be compressed')
    
    convertFile( sys.argv[1], sys.argv[2], sys.argv[3] )

    
