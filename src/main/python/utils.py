'''
Module for utility functions, used commonly in the rest of the HarvardX scripts and programs

Utility functions that are commonly used by HarvardX scripts and programs. Rather
than cut-and-paste these functions, they can be placed in this module and used
throughout.
'''

import os

def getFileName(prompt):
    while (True):
        fname = raw_input('Please enter file name for ' + prompt + ': ')
        if os.path.exists(fname):
            return (fname)
        else:
            print('Entered name does not exist, please retry')
