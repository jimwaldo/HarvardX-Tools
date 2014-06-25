"""
This module contains programs used to convert the data supplied by edX into a form that is more easily
used by the HarvardX research group.

While edX provides considerable research data for courses that are taught using that platform, the
format of that data is somewhat complex and delivered in a fashion that requires some post processing
before it can be used by the research team. The data is provided in two (generally very large) files. 
The first of these, with a name of the form YYYY-MM-DD-HarvardX-tracking.tar, contains the server logs
recording all of the interactions that occur driven from a HarvardX course. The second of these, named
with the form harvardx-YYYY-MM-DD.zip, contains the course-specific data for all courses offered by HarvardX.

These files are generated every week, and the date in the file name indicates the date on which the 
file was generated. The files are first encrypted using a public key provided by the Harvard data czar,
then the encrypted files are zipped together in a single file and placed in an Amazon S3 bucket under 
the directory label course-data. 

Unzipping the log files will create four directories: Harvard, containing logs for any residential 
course; HarvardX, containing the logs for courses offered as MOOCs (even if they are also offered as 
residential); HSPH, containing logs for the school of Public Health; and HarvardKennedySchool, containing
logs for the HKS courses. Each of these directories will contain a directory for the various servers
that have generated the log files, and in each of these directories there will be a log file for each
day, with a name of the form YYYY-MM-DD_Harvard.log. All of these are encrypted.

Processing the log files is done with the script processLogData.sh, which should be run in each of the
high-level directories that is created by unzipping the log file. Currently, edX is shipping all of 
the logs, even those that we have received before. So the first thing that the script does is to enter
each of the server directories and remove any files that are not within a date range that is given (in the
form YYYY-MM-DD) as command-line arguments. Empty directories are then removed, and then the remaining
log files are removed. At that point, all the remaining log files are decrypted, and then a program is 
run that goes through and creates a file for all of the log entries for each class in which an event
was recorded. These log files are named by the class abbreviation. The original log files will be retained
without change. Log entries that have no associated course are added to a file named unknown.log. The 
processing also produces a csv file Classlist.csv, which shows the count of events for each course.

One note: the log file dumps are labeled with the date on which they are generated, and include a log
file for that date. But the files are generated before the end of the day, so the log files for the
day of generation are partial (not knowing this led to some weird data early on). When generating
the log data, the scripts and programs are intended to be run using the date of the last dump (and the
log files for that date will be included, since they are now complete) but will not include the log files
for the second (current) date supplied. So, for example, if the last dump was generated 2014-06-15 and the
current dump on 2014-06-22, the processing of the log files should be 

    processLogData.sh 2014-06-15 2014-06-22
    
which will generate log files including the log from 6/15/14 up to but not including 6/22/14 (which will 
only have some of the log records for that day). 

Unzipping the class data file will produce a directory named harvardx-YYYY-MM_DD. This directory will
contain a number of files for each of the courses that is in the edX database. This includes old courses
that are no longer current, experiments that faculty have tried, courses that haven't yet been launched,
and the currently active courses. The files will all have names that begin HarvardX-, Harvard-, HSPH-, or
HarvardKennedySchool-, followed by a course name/identifier (i.e., PH201x-2014, indicating Public Health 
201, taught during the 2014 academic year) followed by a description of the contents of the file.

This data is processed using the shell script processClassData.sh. The first thing this script does is to
remove as many of the junk, outdated, or extraneous files as it can. This is done with the program
killListedFiles.py, which is something of a hack in that it has a hand-entered and hard-coded list
of the courses that can be removed. The killList in this program specifies a set of patterns that
will be used to delete files. Inactive or junk courses can be found by looking at the ClassList.csv
files produced by the processing of the Log data to find classes in which no events have occurred, but
there is likely a need to consult with the HarvardX group to insure tha you are not adding a new
and not yet active course to the list. There has to be a better way, but I haven't found it.

The script then makes a set of directories to mirror the structure of those created by unpacking the 
log files. It will then move the files that have not been deleted into the appropriate directory,
depending on the prefix of the name of the file. This clusters the files by the entity offering the course,
which is a first step in coming up with something that is useful for the research groups.

The processing continues by going into each of the directories, uncompressing each of the files,
moves the files for each class into a directory named for the class, and then changes the name
of the file to something that (uniformly) represents the contents of the file. Most of these files
are in a tab-separated format that is the result of the extraction from the edX database. Part of
the processing is to create a .csv file from each of these. The files produced, and their contents,
are:
    certificates.{sql, csv}: a listing of all of the users who have received certificates in the course
    enrollment.{sql, csv}: a listing of all users, with some basic demographic information, who 
        have enrolled in the course
    profiles.{sql, csv}: additional demographic information on all who have enrolled in the course
    studentmodule.{sql,csv}: information on progess each student has made in the course
    user_id_map.{sql, csv}: a mapping associating userid, username, and the hashed id of each user
    users.{sql, csv}: information about each user in the course
In addition, there is the course_structure.json file, that represents the components of the course
and their relationships (parent, child) and course.xml.tar.gz, a compressed tarfile that contains
information about the course itself.

Once these files are produced, the program moveWeeklyLoLogs.py should be run from the directory
containing the directories for the various log files and the harvardx-YYYY-MM-DD directory. This
should be run with a first command-line argument that specifies the source files (Harvard, HarvardX,
HSPH, or HarvardKennedySchool) and destination harvardx-YYYY-MM-DD. This will move the weekly logs for
each course into the directory containing the class information for that course.

When all of this is done, the data should be transferred to the IQSS server. We currently use FileZilla
for this.

Once this is done, two more steps are needed to complete setup. These are run on the IQSS servers. 

The first step is to run, in a directory two levels above the raw log files, the program moveRawLogs.py.
This should be given a directory in which all of the raw logs are staged (in our case, this is the directory
at the top level of the shared IQSS data space named AllLogs), This will move all of the raw logs to this
area, where a locally-running cron job will use them to populate the Mongo database used by the researchers.

The second step, run in each of the directories that contain the directories of class data for each
class, is to run the program moveWeeklyToClass.py. This program takes as a first command argument the
destination directory where all of the data on each class is kept; this will (in the IQSS current
setup) be at the top level of the shared space in the directory named Harvard. The second is the
name of a directory in which all of the different class data for the week will be stored (under the Harvard
directory); by convention this is the date of the file download in YYYY-MM-DD format. Once this is
done, the data massaging and re-locating is complete.

"""
