#!/usr/bin/env python 
""" 
Creates a "person-click" CSV dataset for a given logfile and course axis. Relies
heavily on the trackingLogParser module for parsing instructions. Prints a summary
upon completion.

PARAMS: 
    log:            raw edX log file for a particular course
    axis:           course-axis CSV for the relevant course in the logfile
    output:         output CSV file to hold the person-click dataset
    discards:       [optional] output CSV file to which discarded log items are written for debugging
    limit:          [optional] number of lines to parse; default is whole file

PERSON-CLICK OUTPUT:
This is the primary output of this script, structured in an actor-verb-object
format. Each log item, or "event" is parsed into a single row with these columns:
    time            (UTC)
    secs_to_next    (# seconds until the user's next event)
    actor           (username)
    verb            
    object_name
    object_type
    result          
    meta
    ip              (useful for geolocation, or determining local time)
    event           
    event_type      
    page            
    agent           (useful for determining device/OS)

DISCARDS OUTPUT: 
Because many logged events are either redundant (e.g., checking your answer to
a problem triggers up to 4 logged events) or noise (e.g., malformed URLs), the 
trackingLogParser discards many log items. For debugging, you can optionally 
have these discarded log items written to a CSV file with these columns:
    time
    event
    event_type
    page
    username

USAGE:
    python makePersonClick.py CourseLog.log CourseAxis.csv OutputDataset.csv [OutputDiscards.csv] [limit]

WARNING: 
This can be very slow for large log files. Parsing typically runs at a
rate of about 150 MB per minute, so a full course log file of ~10 GB may take 
over an hour to run. Bottleneck comes from the trackingLogParser; working on it.

Created on September 18, 2013

@author: tmullaney
"""

import sys, os
import csv
import json # ujson is faster!
import datetime
import dateutil.parser
from logs import trackingLogParser as tlp

def main():
    # check args
    if(len(sys.argv) < 4):
        print "[Error] Too few arguments"
        return -1

    log = sys.argv[1]
    axis = sys.argv[2]
    output = sys.argv[3]
    discards = sys.argv[4] if len(sys.argv) >= 5 else None
    limit = int(sys.argv[5]) if len(sys.argv) >= 6 else -1

    makePersonClick(axis, log, output, discards, limit)

def parse_time(time_string):
    if(len(time_string) > 5 and time_string[-6:] == "+00:00"): time_string = time_string[:-6]
    return dateutil.parser.parse(str(time_string))

def makePersonClick(axis, log, outpath, outpath_discards=None, limit=-1):
    parser = tlp.LogParser(axis)
    outcsv = csv.writer(open(outpath, "w"))
    outcsv.writerow(["time", "secs_to_next", "actor", "verb", "object_name", "object_type", "result", "meta", "ip", "event", "event_type", "page", "agent"])
    if outpath_discards is not None: 
        outcsv_discards = csv.writer(open(outpath_discards, "w"))
        outcsv_discards.writerow(["time", "event", "event_type", "page", "username"])
    
    activities_without_durations = {} # {username : activity}
    
    # stats
    line_num = 0
    est_total_lines = os.path.getsize(log) / 500 # rough estimate for progress printing
    start_time = datetime.datetime.now()
    unique_verbs = {}
    unique_users = {}
    discard_counts = {}
    total_discards = 0
    total_activities = 0
    start_time = datetime.datetime.now()

    for line in open(log, "r"):
        if(line_num == limit): break
        line_num += 1
        if(line_num % 10000 == 0):
            sys.stdout.write('Lines parsed: %dk/%dk est.\r' % ((line_num/1000), (est_total_lines/1000)))
            sys.stdout.flush()
            
        activity = parser.parseActivity(line)

        if activity is not None:
            total_activities += 1
            if activity["verb"] not in unique_verbs:
                unique_verbs[activity["verb"]] = activity
            if(activity["actor"] not in unique_users):
                unique_users[activity["actor"]] = 1
            
            # record activity
            user = activity["actor"]
            if user in activities_without_durations:
                # calculate difference, record previous activity, and store the new one
                old_activity = activities_without_durations[user]
                activities_without_durations[user] = activity
                time_delta = (parse_time(activity["time"]) - parse_time(old_activity["time"])).total_seconds()
                outcsv.writerow([old_activity["time"], time_delta, old_activity["actor"], old_activity["verb"], old_activity["object"]["object_name"], old_activity["object"]["object_type"], old_activity["result"], old_activity["meta"], old_activity["ip"], old_activity["event"], old_activity["event_type"], old_activity["page"], old_activity["agent"]])
            else:
                # store it to log later
                activities_without_durations[user] = activity
        else:
            total_discards += 1
            log_item_clean = json.loads(line)
            if(log_item_clean["event_type"] not in discard_counts):
                discard_counts[log_item_clean["event_type"]] = 1
            else:
                discard_counts[log_item_clean["event_type"]] += 1
            if outcsv_discards is not None: 
                try: outcsv_discards.writerow([log_item_clean["time"], log_item_clean["event"], log_item_clean["event_type"], log_item_clean["page"], log_item_clean["username"]])
                except UnicodeEncodeError: pass #print log_item_clean
    
    # write remaining activities without durations (will have empty "secs_to_next")
    for k,v in activities_without_durations.items():
        outcsv.writerow([v["time"], None, v["actor"], v["verb"], v["object"]["object_name"], v["object"]["object_type"], v["result"], v["meta"], v["ip"], v["event"], v["event_type"], v["page"], v["agent"]])
    
    print ""
    print "\nSUMMARY\n-------"
    print "total_log_items: " + str(line_num)
    print "total_activities: " + str(total_activities)
    print "total_discards: " + str(total_discards)
    print "pct_discarded: " + str(100.0 * total_discards / line_num) + "%"
    print "unique_users: " + str(len(unique_users.keys()))
    print "unique_verbs: " + str(len(unique_verbs.keys()))
    print "possible_verbs: " + str(len(tlp.possible_verbs))
    print "verbs_not_found: " 
    for v in tlp.possible_verbs:
        if v not in unique_verbs.keys():
            print " - " + v
    end_time = datetime.datetime.now()
    filesize = os.path.getsize(log)/1000000
    if(limit != -1): filesize = "--"
    print "\nParsed " + str(line_num) + " lines (" + str(filesize) + " MB) in " + str((end_time - start_time).total_seconds()) + " sec\n"

if __name__ == "__main__":
    main()