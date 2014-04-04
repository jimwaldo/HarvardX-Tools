#!/usr/bin/env python
'''
Created on Oct 20, 2013

@author: waldo
'''

import os
import glob

killList = ['00001',
            '001-Intro_to_Learning_Management_Eco_System',
            '007Horsey',
            '100',
            '101-My',
            '101-Sept',
            '12345',
            '1795',
            '50000',
            '50-Take_2_on_edX',
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
            'Edelman102',
            'FAS2.1x',
            'Fly_Fishing_',
            'Gov2001',
            'GSE102x',
            'HarvardX-101',
            'HeroesX-HeroesX',
            'HKS-211',
            'HKS211.1x-Central',
            'HLS1x*edge',
            'HS121x-Fall*edge',
            'HSD1544.1x-3T',
            'HX101',
            'ITCx-ITCx',
            'JandR',
            'JS101',
            'JS50',
            'KMH1-Kuriyama_Prototype',
            'Law-LRW_2',
            'SLW1-Legal_Research_for_Non-Lawyers',
            'MCB63',
            'Math101',
            'Mockup',
            'NA_001',
            'NA001',
            'PC10',
            'PH207x-*edge',
            'PH207x-Health',
            'QUANTUM',
            'SAI-HGHI',
            'SHAKE1x',
            'sheep',
            'Sheep',
            'Slow_Cooking_Basics',
            'SP001',
            'SPU17x-3T2013',
            'SPU27X',
            'SW-12X',
            'SW12-ChinaX',
            'SW12x-2013_Oct',
            'SW12.4X',
            'T5532',
            'TBD',
            'test',
            'Test',
            'TR101',
            'Tropicana',
            'TT01x',
            'UH001',
            'WW-TFU1',
            'wiki',
            'WLX',
            'WP1',
            'xxx'
           ]

def killFiles(fileList):
    for f in fileList:
        os.remove(f)
        
if __name__ == '__main__':
    for k in killList:
        l = glob.glob('*'+k+'*')
        killFiles(l)
        