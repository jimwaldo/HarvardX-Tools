#!/usr/bin/env python
"""
Extract the usernames from a JSON file, and write a file of those usernames + event type and event times

Given a file with a field marked 'username', extract the values of those fields
and write, one per line, to a file with the supplied name.
"""
import json
import sys


if __name__ == '__main__':
    f1 = open(sys.argv[1], 'r')
    f2 = open(sys.argv[2], 'w')
    dc = json.JSONDecoder()
    f2.write('username' + ',' + 'event_type' + ',' + 'time' + '\n')
    for line in f1:
        dcl = dc.decode(line)
        f2.write(dcl['username'] + ',' + dcl['event_type'] + ',' + str(dcl['time']) + '\n')


