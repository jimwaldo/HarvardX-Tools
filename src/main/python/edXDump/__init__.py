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
"""
