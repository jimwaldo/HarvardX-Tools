#!/usr/bin/python

'''
This is a file for building a complete list of users who have taken a course
and what they've taken. As such, it's going to be saved as a JSON file.

This is meant to be run from within the repository. Clone the repo into the
/Harvard directory on the shared space, then cd to this local directory and
execute the script. As you can see below, some assumptions are made about the
relative location of things, so it's important to either do as I have outlined
or update the logic below.

@author EJ Bensing
'''

import glob
import buildCompRoster as bcr
import csv
import json

# yah, this isn't the most hacky thing ever... like this is really bad
dirsToExclude = ['Logs', 'LOGS-FROM-2012', 'Unknown', 'idtolocation.csv',
'rosters.tar', 'Course_Axes', 'ebensing-scripts', 'HarvardX-Tools',
'globalis2name.csv', 'globalname2id.csv']

# relative path to the course data top level folder
relPath='../../../../'

# location of the id=>location file, from the relPath directory 
idLocFile='idtolocation.csv'

def main(saveName='StudentCourses.json'):
    # since we're changing the value of the global variable, we need to declare
    # it. I guess python != javascript
    global idLocFile
    global dirsToExclude
    dirsToExclude.append(saveName)
    rdirsToExclude = [relPath + x for x in dirsToExclude]
    idLocFile = relPath + idLocFile
    # get the dirs we're going to search
    courseDirs = [x + '/' for x in glob.glob(relPath + '*') if x not in rdirsToExclude]
   
    # build all of the class roster CSV files
    for courseDir in courseDirs:
        print "Processing " + courseDir
        bcr.main(idLocFile, courseDir)

    rosterFiles = [x + 'FullRoster.csv' for x in courseDirs]
    fullUsers = {}
    # iterate over all of the full class rosters and create the new dict that
    # we'll write out
    for rfile in rosterFiles:
        with open(rfile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                id = row['Student ID']
                if id not in fullUsers:
                    fullUsers[id] = {}
                    fullUsers[id]["courses"] = []
                    for key,val in row.iteritems():
                        # grab all the demographic information except the
                        # student ID since that is the key to the dictionary
                        # anyway
                        if key != 'Student ID':
                            fullUsers[id][key] = val
                
                # hey, what's the worst way we could get the course name? I
                # think this is coming close...
                fullUsers[id]["courses"].append(rfile.replace(relPath,
                    "").replace("FullRoster.csv","").replace("/",""))

    with open(relPath + saveName, 'w') as wfile:
        wfile.write(json.dumps(fullUsers))





if __name__ == '__main__':
    main()
