#!/usr/bin/env python

import csv
import json
import sys

class course_struct:

    def __init__(self, category, children, metad):
        self.category = category
        self.children = children
        self.metad = metad

def getChildNames(dict, entr):
    ent = dict[entr]
    children = ent['children']
    retlist = []
    for c in children:
        retlist.append(dict[c]['metadata']['display_name'])
    return retlist

def save_csv(ctree, f):

    f.writerow(['id', 'category', 'metadata', 'children'])
    for c in iter(ctree):
        chNames = getChildNames(ctree, c)
        f.writerow([ c, ctree[c]['category'], ctree[c]['metadata'], chNames])

inf = open(sys.argv[1], 'r')
inline = inf.readline()
ctdict = json.loads(inline)

outf = csv.writer(open(sys.argv[2], 'w'))
save_csv(ctdict, outf)

    
