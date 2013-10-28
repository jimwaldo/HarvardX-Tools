#!/usr/bin/env python
'''
Created on Oct 20, 2013

@author: waldo
'''

import os
import glob

killList = ['wiki',
            'colin',
            'Colin',
            'Dummy',
            'test',
            'Test',
            'Dogs',
            '12345',
            'Demo',
            'sheep',
            'Sheep'
            ]

def killFiles(fileList):
    for f in fileList:
        os.remove(f)
        
if __name__ == '__main__':
    for k in killList:
        l = glob.glob('*'+k+'*')
        killFiles(l)
        