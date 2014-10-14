#!/usr/bin/env python
"""
  This file is a master lookup list for the following:
  - Known Hosts
       List of known valid hosts from EdX for which to parse
  - Known Organization Id's
       List of known Organization's that will define the top level directory structure
       This is also known as the list of School Names
  - Joint Harvard/MIT Courses
       List of courses that are common between Harvard/MIT
       This file is needed since the course_id for Harvard/MIT common courses
       have the format as follows: "VJx/VJx"
"""
from killListedFiles import *

# Known Hosts
known_host_names = [\
	'courses.edx.org',
	'edge.edx.org']

# Known Org Id's (School names)
known_org_ids = [\
	'Harvard',
	'HarvardX',
	'HarvardKennedySchool',
	'HSPH']

# Known joint Harvard/MIT Courses
known_HarvardMIT_courses = {'VJx': 'HarvardX'
                            }

