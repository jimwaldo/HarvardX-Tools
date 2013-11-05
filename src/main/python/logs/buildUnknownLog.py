#!/usr/bin/env python
'''
Created on Nov 3, 2013

@author: waldo
'''

import glob
import json
import buildWeekLog as blog

if __name__ == '__main__':
    logFiles = glob.glob('prod*/unknown*')
    fLog = blog.combineLogs('unknown', logFiles)
    blog.writeCombLog('unknownProd.log', fLog)