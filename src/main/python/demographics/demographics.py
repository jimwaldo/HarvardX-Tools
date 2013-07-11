#!/usr/bin/env python
'''
Created on Mar 7, 2013

Create a report on the demographics of a course, and create an anonymized
csv file for the students in the course. The demographics include the gender and
age distribution, level of education, and the country of the student. All of
the information is self-reported, and so is somewhat suspect. The location
information is extracted from the self-reported mailing address; this could
be the physical mailing address or the email address (and is often left blank).

Usage
    demographics.py classname file
    where
        classname is the name of the course, used to print out the report 
            heading
        file is the csv file containing the user demographic information 
            for the students in the course (user_profile)
    The program will create a file with the same name, with 'anon_' as a prefix

@author: waldo
'''

import userprofile as prof
import sys
import csv
import ipGeoloc as geo
import utils


def makeCountryDict(fin, filename):
    idC = csv.reader(open(filename, 'r'))
    return geo.buildIdtoLoc(fin, idC)
    
def writeAnon(outf, p):
    '''
    Write an anonymized version of the data into a line of a csv file
    
    This function will create a file with the user profile data, stripped of
    identifying information (the user_id, name, and address of the student)
    All that is left is the gender, the year of birth, the level of education,
    and the self-reported goal for taking the course.
    
    Parameters
    ----------
    outf: csv.writer 
        File in which to place the anonymized data
    p: profile
        The full profile information for the student
    '''
    outf.writerow([p.gender, p.yob, p.ledu, p.goal])
    
male = female = undisc = 0
countries = {}
ages = {}
edu = {'p_se':0,
       'p_oth':0,
       'm':0,
       'b':0,
       'hs':0,
       'jhs':0,
       'el':0,
       'none':0,
       'other':0,
       'unk':0
       }
        
csv.field_size_limit(1000000000)
clName = sys.argv[1]
ufile = utils.getFileName('user file')
ufin = csv.reader(open(ufile, 'r'))
profile_file = utils.getFileName('student profiles')
infile = csv.reader(open(profile_file, 'r'))
profiles = prof.builddict(infile)
countryFile = utils.getFileName('username and country file')
countryDict = makeCountryDict(ufin, countryFile)
outName = raw_input("enter file name for output; nothing for stdout : ")
if outName == '':
    outp = sys.stdout.write
else:
    outFile = open(outName, 'w')
    outp = outFile.write
outfile = csv.writer(open('anon'+sys.argv[1], 'w'))

students = profiles.keys()

for s in students:
    if profiles[s].gender == 'm':
        male += 1
    elif profiles[s].gender == 'f':
        female += 1
    else:
        undisc += 1
        
    if (s in countryDict):
        where = countryDict[s]
    else:
        where = None
        
    if where == None:
        where = 'unknown'
    if where not in countries:
        countries[where] = 1
    else:
        countries[where] += 1
        
    ed = profiles[s].ledu
    if ed in edu:
        edu[ed] += 1
    else:
        edu['unk'] += 1
    yb = profiles[s].yob
    if yb.isdigit():
        age = 2013 - int(yb)
        if age not in ages:
            ages[age] = 0
        ages[age] += 1
    writeAnon(outfile, profiles[s])
        
outp("Demographic information for " + clName + '\n')
outp( 'Gender distribution:' + '\n')
outp( '\tMale : ' + str(male) + '\n')
outp( '\tFemale : ' + str(female) + '\n')
outp( '\tunspecified : ' + str(undisc)+ '\n')
outp( '\tTotal : ' + str(male + female + undisc) + '\n')
outp(''+ '\n')
outp( 'Reported education level'+ '\n')
outp( '\tPh.D. in science or engineering : ' + str(edu['p_se'])+ '\n')
outp( '\tPh.D. in another field : ' + str(edu['p_oth'])+ '\n')
outp( '\tMaster or professional degree : ' + str(edu['m'])+ '\n')
outp( '\tBachelor degree : ' + str(edu['b'])+ '\n')
outp( '\tSecondary/high school : ' + str(edu['hs'])+ '\n')
outp( '\tJunior high school : ' + str(edu['jhs'])+ '\n')
outp( '\tElementary school : ' + str(edu['el'])+ '\n')
outp( '\tNone : ' + str(edu['none'])+ '\n')
outp( '\tOther : ' + str(edu['other'])+ '\n')
outp(''+ '\n')
outp( 'Participants by age'+ '\n')
ca = sorted(ages.keys())
for a in ca:
    outp( '\t' + str(a) + ' : ' + str(ages[a])+ '\n')
outp( ''+ '\n')
outp( 'Participants by country'+ '\n')
ct = sorted(countries.keys())
for c in ct:
    outp('\t' + c + ' : ' + str(countries[c])+ '\n')
outp( ''+ '\n')


    
