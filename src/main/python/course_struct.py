#!/usr/bin/env python
"""
Build a csv file reflecting the course structure, using the edX supplied json file.


"""
import csv
import json
import sys


class course_struct:

    def __init__(self, category, children, metad):
        self.category = category
        self.children = children
        self.metad = metad

def getChildNames(dct, entr):
    ent = dct[entr]
    children = ent['children']
    retlist = []
    for c in children:
        retlist.append(dct[c]['metadata']['display_name'])
    return retlist

def save_csv(ctree, f):

    f.writerow(['id', 'category', 'metadata', 'children'])
    for c in iter(ctree):
        chNames = getChildNames(ctree, c)
        f.writerow([ c, ctree[c]['category'], ctree[c]['metadata'], chNames])

if __name__ == '__main__':
    if len(sys.argv != 3):
        print "Usage: course_struct.py courseFile.json outFile.csv"
        sys.exit(1)
        
    inf = open(sys.argv[1], 'r')
    inline = inf.readline()
    ctdict = json.loads(inline)

    outf = csv.writer(open(sys.argv[2], 'w'))
    save_csv(ctdict, outf)

    
