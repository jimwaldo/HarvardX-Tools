#!/usr/bin/env python
"""
Combines all of the log entries from the various servers that have been found 
that have no known class association into a single file.

@author: waldo
"""

import glob
import json
from edXDump import buildWeekLog as blog

if __name__ == '__main__':
    logFiles = glob.glob('prod*/unknown*')
    fLog = blog.combineLogs('unknown', logFiles)
    blog.writeCombLog('unknownProd.log', fLog)