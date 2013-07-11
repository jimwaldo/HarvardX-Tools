#!/usr/bin/env python
'''
Converts tab-separated lines from the data dumps into a csv file. 
The program takes an sql file and the name of the csv file to 
be produced. 

Created on Apr 7, 2013

@author: waldo
'''

if __name__ == '__main__':
    pass

import sys
import csv

if (len(sys.argv) < 3):
    print ('Usage: sqltocsv.py file1 file2 where')
    print ('file1 is an existing .sql file from edx and')
    print ('file2 is the name of the .csv file to produce')
f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'w')
f3 = csv.writer(f2)

for line in f1:
    f3.writerow(line[:-1].split('\t'))
    
f1.close()
f2.close()
