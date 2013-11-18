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
            'Sheep', 
            '100',
            'HarvardX-101',
            'TBD',
            'PC10',
            'QUANTUM',
            'JS50',
            'WP1',
            'WLX',
            'TR101',
            'Math101',
            'Biblical_Literacy',
            'Gov2001',
            'AIU12x',
            'AV101',
            '1795',
            '101-Sept',
            '50000',
            'HSD1544.1x-3T',
            'HeroesX-HeroesX',
            'HLS1x*edge',
            'HS121x-Fall*edge',
            'NA_001',
            'Mockup',
            'SPU27X',
            'HKS-211',
            'HKS211.1x-Central',
            'SW12-ChinaX',
            'SW-12X'
            'SW12x-2013_Oct',
            'TT01x',
            'PH207x-Health',
            'PH207x-*edge',
            'CB22x*edge'
            ]

def killFiles(fileList):
    for f in fileList:
        os.remove(f)
        
if __name__ == '__main__':
    for k in killList:
        l = glob.glob('*'+k+'*')
        killFiles(l)
        