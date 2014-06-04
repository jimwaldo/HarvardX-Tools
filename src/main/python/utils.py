'''
Module for utility functions, used commonly in the rest of the HarvardX scripts and programs

Utility functions that are commonly used by HarvardX scripts and programs. Rather
than cut-and-paste these functions, they can be placed in this module and used
throughout.
'''

import os
'''
Get the name of an existing file. If the file does not exist, the user will be 
prompted to re-enter the filename. Returns a string.
'''
def getFileName(prompt):
    while (True):
        fname = raw_input('Please enter file name for ' + prompt + ': ')
        if os.path.exists(fname):
            return (fname)
        else:
            print('Entered name does not exist, please retry')
'''
Get the name of a new file, insuring that no file of that name already exists.
If a file of that name exists, the user will be propted to re-enter the filename.
Returns a string
'''
def getNewFileName(prompt):
    while (True):
        fname = raw_input('Please enter file name for ' + prompt + ' : ')
        if os.path.exists(fname):
            print ('Entered name already exists; please enter the name of a new file')
        else:
            return (fname)
        
'''
Display a prompt and get an integer value from the user, after showing the supplied prompt. 

If the user enters something other than an integer, they will be asked to enter an integer 
and re-prompted
'''        
def getIntVal(prompt):
    while(True):
        inVal = raw_input(prompt)
        try:
            return(int(inVal))
        except:
            print('please enter an integer value')
            
'''
Display a prompt and get a string back, which is then checked against a list of string values.

If the string entered is not one of the values checked against, the user will be re-prompted.
Returns a string
'''
def getStringVal(prompt, acceptList):
    while (True):
        retStr = raw_input(prompt)
        if retStr in acceptList:
            return retStr
        else:
            print('invalid entry, please re-try')
            
