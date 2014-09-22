#!/usr/bin/env python
'''
Created on Sep 19, 2014

@author: waldo
'''
import glob
import subprocess

def findNewFiles():
    """
    Find all of the files that have been downloaded, and then determine all of
    those that have not been decrypted. Return a list of those that need to be
    decrypted now. 
    """
    allFiles = glob.glob('*.gpg')
    oldFiles = glob.glob('*.gz')
    retFiles = []
    for f in allFiles:
        if f[:-4] not in oldFiles:
            retFiles.append(f)
    return retFiles

def deComp(f):
    """
    Decrypt the file named by the string passed in. The decryption is done
    by making a subprocess call to gpg, but could be changed in the future.
    """
    subprocess.call(['gpg','-o', f[:-4], '-d', f] )

if __name__ == '__main__':
    newFiles = findNewFiles()
    for f in newFiles:
        print f
        deComp(f)
        
    