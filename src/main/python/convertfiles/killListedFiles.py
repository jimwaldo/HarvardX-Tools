#!/usr/bin/env python
'''
Created on Oct 20, 2013

@author: waldo
'''

import os
import glob

killList = ['00001',
            '007Horsey',
            '100',
            '101-My',
            '101-Sept',
            '12345',
            '1795',
            '50000',
            'AIU12x',
            'AV101',
            'Biblical_Literacy',
            'CB22x*edge',
            'colin',
            'Colin',
            'Demo',
            'Dogs',
            'DOGS',
            'Dummy',
            'Fly_Fishing_',
            'Gov2001',
            'HarvardX-101',
            'HeroesX-HeroesX',
            'HKS-211',
            'HKS211.1x-Central',
            'HLS1x*edge',
            'HS121x-Fall*edge',
            'HSD1544.1x-3T',
            'JandR',
            'JS50',
            'Math101',
            'Mockup',
            'NA_001',
            'PC10',
            'PH207x-*edge',
            'PH207x-Health',
            'QUANTUM',
            'sheep',
            'Sheep', 
            'SPU27X',
            'SW-12X'
            'SW12-ChinaX',
            'SW12x-2013_Oct',
            'TBD',
            'test',
            'Test',
            'TR101',
            'Tropicana',
            'TT01x',
            'wiki',
            'WLX',
            'WP1'
           ]

def killFiles(fileList):
    for f in fileList:
        os.remove(f)
        
if __name__ == '__main__':
    for k in killList:
        l = glob.glob('*'+k+'*')
        killFiles(l)
        