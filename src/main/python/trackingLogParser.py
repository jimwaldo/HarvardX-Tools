#!/usr/bin/env python 
''' 
Class/module for parsing Tracking Log events into a standardized
ExperienceAPI/TinCan-style schema with the following fields:

    actor:      username
    verb:       problem_check/video_play/etc.
    object:     varies for different verbs (courseware_name, forum_hash, user_id, search_term, etc.)
    result:     often None, or the user's answer to a poll, or a problem answer's correctness
    meta:       varies; for videos, includes playback speed
    time:       timestamp

    ip:         for geolocation
    event:      for debugging
    event_type: for debugging
    page:       for debugging
    agent:      for device/OS info

NOTE:
This is functional, but very much a work in progress; ugly, complex,
and slow. Need to figure out the best way to manage these tradeoffs.

Created on September 18, 2013

@author: tmullaney
'''

import re
import csv
import json # ujson faster?

# list manually maintained
possible_verbs = ["annotation_create"
                    ,"book_view"
                    #,"email" # unreliable and not used for now
                    ,"forum_close"
                    ,"forum_create"
                    ,"forum_delete"
                    ,"forum_downvote"
                    ,"forum_endorse"
                    ,"forum_flag_abuse"
                    ,"forum_follow"
                    ,"forum_pin"
                    ,"forum_reply"
                    ,"forum_search"
                    ,"forum_unflag_abuse"
                    ,"forum_unfollow"
                    ,"forum_unpin"
                    ,"forum_unvote"
                    ,"forum_update"
                    ,"forum_upvote"
                    ,"forum_view"
                    ,"forum_view_followed_threads"
                    ,"forum_view_inline"
                    ,"forum_view_user_profile"
                    ,"page_view"
                    ,"page_close"
                    ,"poll_answer"
                    ,"poll_view"
                    ,"problem_check"
                    ,"problem_save"
                    ,"problem_view"
                    ,"seq_goto"
                    ,"seq_next"
                    ,"seq_prev"
                    ,"video_pause"
                    ,"video_play"
                    ,"wiki_view"]

# TODO: ADD THESE TO COURSE AXIS (?)
# top-level tabs are not available in course axes so I've hard-coded them in here; 
# needs to be updated for any new courses with custom top-level pages;
# maps the page's last url slug to the tab's display name
top_level_tabs = {
    # General
    "info" : "Course Info"
    ,"progress" : "Progress"
    ,"notes" : "My Notes"
    ,"open_ended_notifications" : "Open Ended Panel"
    ,"instructor" : "Instructor"
    ,"about" : "About" # where is this page? (/courses/HarvardX/ER22x/2013_Spring/about)

    # CB22x/2013_Spring
    ,"01356a17b5924b17a04b7fc2426a3798" : "Syllabus"
    ,"57e9991c0d794ff58f7defae3e042e39" : "Advice for Participants"

    # ER22x/2013_Spring
    ,"7a8a540432444be59bd3b6a6ddf725ff" : "Weekly Forum Digest"
    ,"677191905f71448aab5346a3ed038f87" : "Frequently Asked Questions"

    # PH278x/2013_Spring
    ,"1e7a1201a4214fbaa1d675393c61be5f" : "Syllabus"
    ,"861a584197fc40a1af55117629d087b8" : "Textbook"
    ,"782c7c85b9784de5a18199d1c2eaedfa" : "Readings"
    ,"73f5c222bdc3440bb8dd0423c86e219d" : "Solution Discussion Groups"

    # PH207x/2012_Fall
    ,"datasets" : "Data Sets"
    ,"faq" : "FAQ"

    # CS50x/2012
    ,"discuss" : "CS50 Discuss"
    ,"gradebook" : "CS50 Gradebook"
    ,"spaces" : "CS50 Spaces"

    # HLS1x[A|B|C|D]/Copyright
    ,"Logistics" : "Logistics"
    ,"Syllabus" : "Syllabus"
    ,"Resources" : "Resources"
    ,"Staff" : "Course Staff and Teaching Fellows"
}

# REGEX
# global so not recompiling each time
# all verb regex should be applied to event_type unless otherwise noted
re_hash = re.compile("[0-9a-f]{24,32}")

re_video_play = re.compile("^play_video$")
re_video_pause = re.compile("^pause_video$")

re_seq_goto = re.compile("^seq_goto$")
re_seq_next = re.compile("^seq_next$")
re_seq_prev = re.compile("^seq_prev$")

re_poll_view = re.compile("poll_question\/[^/]+\/get_state")
re_poll_answer = re.compile("poll_question\/[^/]+\/(?!get_state).+")

re_problem_view = re.compile("problem\/[^/]+\/problem_get$")
re_problem_save_success = re.compile("^save_problem_success$")
re_problem_save_fail = re.compile("^save_problem_fail$")
re_problem_check = re.compile("^problem_check$") # we want the server event b/c contains correctness info
re_problem_check2 = re.compile("^save_problem_check$") # also needs to be a server event
re_problem_show_answer = re.compile("^showanswer$")

re_wiki_view = re.compile("wiki")

#re_email = re.compile("[^@]+@[^@]+\.[^@]+")

re_annotation_create = re.compile("notes\/api\/annotations$") # see POST for object
re_book_view = re.compile("notes\/api\/search$") # used in CB22x; not the normal textbook module

re_forum_view = re.compile("discussion\/forum$") # view threads
re_forum_view_user_profile = re.compile("discussion\/forum\/users\/[^/]+$")
re_forum_view_followed_threads = re.compile("discussion\/forum\/users\/[^/]+\/followed$")
re_forum_search = re.compile("discussion\/forum\/search$") # also used when selecting from dropdown

re_forum_thread_view_inline = re.compile("discussion\/forum\/[^/]+\/inline$") # view thread from courseware
re_forum_thread_view = re.compile("discussion\/forum\/[^/]+\/threads\/[^/]+$") # retrieve_single_thread (permanent_link_thread)
re_forum_thread_create = re.compile("discussion\/[^/]+\/threads\/create$")
re_forum_thread_close = re.compile("discussion\/threads\/[^/]+/close$")
re_forum_thread_delete = re.compile("discussion\/threads\/[^/]+/delete$")
re_forum_thread_downvote = re.compile("discussion\/threads\/[^/]+/downvote$")
re_forum_thread_flag_abuse = re.compile("discussion\/threads\/[^/]+/flagAbuse$")
re_forum_thread_follow = re.compile("discussion\/threads\/[^/]+/follow$")
re_forum_thread_pin = re.compile("discussion\/threads\/[^/]+/pin$")
re_forum_thread_reply = re.compile("discussion\/threads\/[^/]+/reply$") # create comment
re_forum_thread_unflag_abuse = re.compile("discussion\/threads\/[^/]+/unFlagAbuse$")
re_forum_thread_unfollow = re.compile("discussion\/threads\/[^/]+/unfollow$")
re_forum_thread_unpin = re.compile("discussion\/threads\/[^/]+/unpin$")
re_forum_thread_unvote = re.compile("discussion\/threads\/[^/]+/unvote$")
re_forum_thread_update = re.compile("discussion\/threads\/[^/]+/update$")
re_forum_thread_upvote = re.compile("discussion\/threads\/[^/]+/upvote$")

re_forum_comment_delete = re.compile("discussion\/comments\/[^/]+/delete$")
re_forum_comment_downvote = re.compile("discussion\/comments\/[^/]+/downvote$")
re_forum_comment_endorse = re.compile("discussion\/comments\/[^/]+/endorse$")
re_forum_comment_flag_abuse = re.compile("discussion\/comments\/[^/]+/flagAbuse$")
re_forum_comment_reply = re.compile("discussion\/comments\/[^/]+/reply$")
re_forum_comment_unflag_abuse = re.compile("discussion\/comments\/[^/]+/unFlagAbuse$")
re_forum_comment_unvote = re.compile("discussion\/comments\/[^/]+/unvote$")
re_forum_comment_update = re.compile("discussion\/comments\/[^/]+/update$")
re_forum_comment_upvote = re.compile("discussion\/comments\/[^/]+/upvote$")

re_page_view_courseware = re.compile("courseware\/[^/]+([^/]+)*\/?")
re_page_view_main = re.compile("courses\/[^/]+\/[^/]+\/[^/]+\/[^/]+") # very general, run after everything else
re_page_close = re.compile("^page_close$")


# PARSER OBJECT
# parameterized by a course axis (for identifying objects)
# where axis csv line format is as follows:
# ["index","url_name","category","gformat","start","due","name","path","module_id","data"]
class Parser:
    def __init__(self, axis_csv):
        '''
        An Parser instance is particular to a course. Initialize by passing
        the relevant Course Axis (.CSV), which is used for identifying objects.
        '''

        # we need to build two axis lookup dicts
        self.axis_path_to_courseware_name = {} # used for page_view and page_close
        self.axis_url_name_to_courseware_name = {} # used for everything else
        current_chapter = ""
        current_sequential = ""
        current_vertical = ""
        row_num = 0
        for line in csv.reader(open(axis_csv)):
            row_num += 1
            if(row_num < 3): continue # first two rows are headers and "course"
            
            url_name = line[1]
            category = line[2]
            name = line[6]
            path = line[7]
            courseware_name = ""

            if(category == "chapter"): 
                current_chapter = name
                courseware_name = current_chapter
            elif(category == "sequential"): 
                current_sequential = name
                courseware_name = "/".join([current_chapter, current_sequential])
            elif(category == "vertical"): 
                current_vertical = name
                courseware_name = "/".join([current_chapter, current_sequential, current_vertical])
            else:
                # category is a resource
                # courseware_name looks like: {chapter}/{sequential}/{vertical}/{resource}
                # sometimes redundant, but most reliable way of uniquely and meaningfully identifying objects
                courseware_name = "/".join([current_chapter, current_sequential, current_vertical, name])

            self.axis_path_to_courseware_name[path] = courseware_name
            self.axis_url_name_to_courseware_name[url_name] = courseware_name

    def parseActivity(self, log_item):
        '''
        Parses an ExperienceAPI/TinCan-esque Activity (actor, verb, object, result, meta)
        from a single JSON-formatted log entry (as a string). Returns a dictionary 
        if activity can be parsed, None otherwise.
        '''
        # convert log_item string into dict
        log_item_json = json.loads(log_item)

        try:
            event = str(log_item_json["event"]) # cast to string b/c as dict isn't consistent in logs
            event_type = log_item_json["event_type"]
            page = log_item_json["page"]
        except Exception:
            # malformed log_item
            return None

        try:
            e = json.loads(event)
            e_get = e["GET"]
            e_post = e["POST"]
        except ValueError:
            # json object couldn't be decoded
            # "event" field is truncated/malformed
            pass
        except KeyError:
            # "event" field doesn't have a GET/POST field
            pass
        except TypeError:
            # "event" field is just a string (no key/value pairs)
            pass

        ### VIDEO ###
        # TODO: is a specific event logged when the user changes playback speed?
        # TODO: add video_duration to course axes and to the meta field here (use YouTube API)
        if(re_video_play.search(event_type) or re_video_pause.search(event_type)):
            # (note: video_play and video_pause are identical other than the verb name)
            # event_type: [browser] "play_video"
            # event: "{"id":"i4x-HarvardX-CB22x-video-39c9cccdd02846d998ae5cd894830626","code":"YTOR7kAvl7Y","currentTime":279.088,"speed":"1.0"}"
            v = "video_play" if "play_video" == event_type else "video_pause"
            o = self.__getCoursewareObject(event.split("video-")[1].split("\"")[0])
            r = None
            m = {"youtube_id": e["code"]}
            try: m["playback_speed"] = e["speed"]
            except KeyError: m["playback_speed"] = None
            try: m["playback_position_secs"] = e["currentTime"] # sometimes this field is missing
            except KeyError: m["playback_position_secs"] = None

        ### SEQUENTIAL ###
        # TODO: give better names to the meta 'new' and 'old' fields (currently just ints)
        elif(re_seq_goto.search(event_type) or re_seq_next.search(event_type) or re_seq_prev.search(event_type)):
            # (note: seq_goto, seq_prev, and seq_next are identical other than the verb name)
            # when a user navigates via sequential, two events are logged...
            # event_type: [server] "/courses/HarvardX/ER22x/2013_Spring/modx/i4x://HarvardX/ER22x/sequential/lecture_01/goto_position"
            # event_type: [browser] "seq_goto" <-- we use this one
            # event: "{"old":1,"new":2,"id":"i4x://HarvardX/CB22x/sequential/fed323e44ab14407907a7f401f1bfa87"}"
            v = event_type
            try: o = self.__getCoursewareObject(event.split("sequential/")[1].split("\"")[0])
            except IndexError: 
                o = self.__getCoursewareObject(event.split("videosequence/")[1].split("\"")[0]) # used in PH207x
            r = None
            m = {
                "new": e["new"],
                "id": e["id"]
            } 
            try: m["old"] = e["old"] # sometimes the "old" field is missing
            except KeyError: m["old"] = None

        ### POLL ###
        elif(re_poll_view.search(event_type)): 
            # (note: polls are often wrapped by conditionals, but we don't log any events for conditionals)
            # logged when a poll is loaded onscreen (whether answered or not); sometimes several at once
            # event_type: [server] "/courses/HarvardX/ER22x/2013_Spring/modx/i4x://HarvardX/ER22x/poll_question/T13_poll/get_state"
            v = "poll_view"
            o = self.__getCoursewareObject(event_type.split("/")[-2])
            r = None
            m = None
        elif(re_poll_answer.search(event_type)):
            # logged when user clicks a poll answer; "result" field can be 'yes', 'no', or any other answer value
            # event_type: [server] "/courses/HarvardX/ER22x/2013_Spring/modx/i4x://HarvardX/ER22x/poll_question/T7_poll/yes"
            v = "poll_answer"
            split = event_type.split("/")
            o = self.__getCoursewareObject(split[-2])
            r = split[-1]
            m = None

        ### PROBLEM (CAPA) ###
        elif(re_problem_view.search(event_type)):
            # logged when a problem is loaded onscreen; often several at once
            # event_type: [server] "/courses/HarvardX/CB22x/2013_Spring/modx/i4x://HarvardX/CB22x/problem/bb8a422a718a4788b174220ed0e9c0d7/problem_get"
            v = "problem_view"
            o = self.__getCoursewareObject(event_type.split("problem/")[1].split("/")[0])
            r = None
            m = None
        elif((re_problem_check.search(event_type) or re_problem_check2.search(event_type)) and log_item_json["event_source"] == "server"):
            # when a user clicks 'Check,' three events are logged...
            # event_type: [browser] "problem_check"
            # event_type: [server] "/courses/HarvardX/CB22x/2013_Spring/modx/i4x://HarvardX/CB22x/problem/249d6f5aa35d4c0e850ece425676eacd/problem_check"
            # event_type: [server] "save_problem_check" OR "problem_check" <-- we use this one b/c event field contains correctness info
            v = "problem_check"
            o = self.__getCoursewareObject(event.split("problem/")[1].split("'")[0])
            r = event.split("'")[3] # value of key "success"
            m = None
        elif(re_problem_save_success.search(event_type) or re_problem_save_fail.search(event_type)):
            # when a user clicks 'Save,' three events are logged...
            # event_type: [browser] "problem_save"
            # event_type: [server] "/courses/HarvardX/CB22x/2013_Spring/modx/i4x://HarvardX/CB22x/problem/4c26fb3fcef14319964d818d73cc013d/problem_save"; 
            # event_type: [server] "save_problem_success" OR "save_problem_fail" <-- we use this one to capture success
            v = "problem_save"
            o = self.__getCoursewareObject(event.split("problem/")[1].split("'")[0])
            r = "success" if event_type.split("problem_")[1] == "save" else "fail"
            m = None
        elif(re_problem_show_answer.search(event_type)):
            v = "problem_view"
            o = self.__getCoursewareObject(event.split("problem/")[1].split("'")[0])
            r = None
            m = None

        ### WIKI ###
        # TODO: flesh this out with better object names
        elif(re_wiki_view.search(event_type)):
            v = "wiki_view"
            o_name = event_type
            o = {
                "object_type" : "url",
                "object_name" : o_name
            }
            r = None
            m = None

        ### EMAIL ### 
        # TODO: not particularly reliable; leaving out for now
        # problematic example: event_type = /courses/HarvardX/CB22x/2013_Spring/submission_history/mary.finn@oir.ie/i4x://HarvardX/CB22x/problem/6f869b8bb1e04ec5b2106afc80708c9b
        # elif(re_email.search(event_type)):
        #     v = "email"
        #     o_name = event_type.split("/")[-1]
        #     o = {
        #         "object_type" : "email",
        #         "object_name" : o_name
        #     }
        #     r = None
        #     m = None

        ### ANNOTATION ### (only in CB22x)
        # TODO: annocation_edit and annotation_delete -- requires looking at multiple events at once (difficult with current framework)
        elif(re_annotation_create.search(event_type)):
            # when the user 'Save's an annotation, two events are logged
            # event_type: [server] https://courses.edx.org/courses/HarvardX/CB22x/2013_Spring/notes/api/annotations <-- use this one b/c has post info in event field
            # event_type: [server] https://courses.edx.org/courses/HarvardX/CB22x/2013_Spring/notes/api/annotations/38650 
            v = "annotation_create"
            try:
                s = event.split("uri\\\":\\\"")[1]
                uri = s.split("\\\"")[0]
                o_name = uri
            except Exception:
                o_name = "[Unavailable]" # sometimes the annotation text is too long and the rest gets truncated
            o = {
                "object_type" : "asset_id",
                "object_name" : o_name
            }
            r = None
            m = None

        ### BOOK ###
        # TODO: add support for PH207x PDF book (unable to test)
        elif(re_book_view.search(event_type)):
            # we infer book view events from the annotation module, which logs the following every page load:
            # event_type: [server] "/courses/HarvardX/CB22x/2013_Spring/notes/api/search"
            # event: "{"POST": {}, "GET": {"limit": ["0"], "uri": ["/c4x/HarvardX/CB22x/asset/book_sourcebook_herodotus-kyrnos.html"]}}"     
            v = "book_view"
            try:
                s = event.split("uri\": [\"")[1]
                uri = s.split("\"")[0]
                o_name = uri
            except Exception:
                o_name = "[Unavailable]"
            o = {
                "object_type" : "asset_id",
                "object_name" : o_name
            }
            r = None
            m = None

        ### FORUM - TOP LEVEL ###
        # TODO: clean this mess up!!
        # TODO: come up with way to give forum hashes human-readable names
        elif(re_forum_view.search(event_type)):
            v = "forum_view"
            o_name = self.__getHashPath(event_type)
            if(o_name == ""): o_name = None
            o = {
                "object_type" : "forum_hash",
                "object_name" : o_name
            }
            r = None
            try: 
                m = {
                    "sort_key": e_get["sort_key"][0],
                    "sort_order": e_get["sort_order"][0],
                    "page": e_get["page"][0]
                }
            except KeyError:
                m = None # sometimes there won't be anything in the "event"
        elif(re_forum_view_followed_threads.search(event_type)):
            v = "forum_view_followed_threads"
            o_name = ("".join(event_type.split("users/")[1:]).split("/")[0]) # user id is the trailing number
            o = {
                "object_type" : "forum_user_id",
                "object_name" : o_name
            }
            r = None
            m = {
                "sort_key": e_get["sort_key"][0],
                "sort_order": e_get["sort_order"][0],
                "page": e_get["page"][0]
            }
            try: m["group_id"] = e_get["group_id"]
            except KeyError: m["group_id"] = None
        elif(re_forum_view_user_profile.search(event_type)):
            v = "forum_view_user_profile"
            o_name = "".join(event_type.split("users/")[1:]) # user id is the trailing number
            o = {
                "object_type" : "forum_user_id",
                "object_name" : o_name
            }
            r = None
            m = None
        elif(re_forum_search.search(event_type)):
            v = "forum_search"
            r = None
            try: 
                m = {
                    "text": e_get["text"][0].encode("utf-8"),
                    "sort_key": None,
                    "sort_order": None,
                    "page": None
                }
            except KeyError:
                m = {
                    "sort_key": e_get["sort_key"][0],
                    "sort_order": e_get["sort_order"][0],
                    "page": e_get["page"][0]
                }
                try: m["text"] = e_get["commentable_ids"][0].encode("utf-8"),
                except KeyError: m["text"] = None
            o_name = m["text"]
            o = {
                "object_type" : "search_text",
                "object_name" : o_name
            }

        ### FORUM - THREADS ###
        # (note: thread and comment events are coded separately in case we want to break apart later)
        elif(re_forum_thread_create.search(event_type)):
            v = "forum_create"
            o = self.__getForumObject(event_type)
            r = None
            m = None # we could put the new thread's text here...
        elif(re_forum_thread_close.search(event_type)):
            v = "forum_close"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_delete.search(event_type)):
            v = "forum_delete"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_downvote.search(event_type)):
            v = "forum_downvote"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_flag_abuse.search(event_type)):
            v = "forum_flag_abuse"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_follow.search(event_type)):
            v = "forum_follow"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_pin.search(event_type)):
            v = "forum_pin"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_reply.search(event_type)):
            v = "forum_reply"
            o = self.__getForumObject(event_type)
            r = None
            m = None # we could put the new comment's text here...
        elif(re_forum_thread_unflag_abuse.search(event_type)):
            v = "forum_unflag_abuse"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_unfollow.search(event_type)):
            v = "forum_unfollow"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_unpin.search(event_type)):
            v = "forum_unpin"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_unvote.search(event_type)):
            v = "forum_unvote"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_update.search(event_type)):
            v = "forum_update"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_upvote.search(event_type)):
            v = "forum_upvote"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_view_inline.search(event_type)):
            v = "forum_view_inline"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_thread_view.search(event_type)):
            v = "forum_view"
            o = self.__getForumObject(event_type)
            r = None
            m = None

        ### FORUM - COMMENTS ###
        elif(re_forum_comment_delete.search(event_type)):
            v = "forum_delete"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_comment_downvote.search(event_type)):
            v = "forum_downvote"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_comment_endorse.search(event_type)):
            v = "forum_endorse"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_comment_flag_abuse.search(event_type)):
            v = "forum_flag_abuse"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_comment_reply.search(event_type)):
            v = "forum_reply" 
            o = self.__getForumObject(event_type)
            r = None
            m = None # we could put the new comment's text here...
        elif(re_forum_comment_unflag_abuse.search(event_type)):
            v = "forum_unflag_abuse"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_comment_unvote.search(event_type)):
            v = "forum_unvote"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_comment_update.search(event_type)):
            v = "forum_update"
            o = self.__getForumObject(event_type)
            r = None
            m = None
        elif(re_forum_comment_upvote.search(event_type)):
            v = "forum_upvote"
            o = self.__getForumObject(event_type)
            r = None
            m = None

        ### PAGE ### 
        # need to make sure these objects can be found in course axes; otherwise, likely just noise/malformed urls
        elif(re_page_view_courseware.search(event_type)):
            # page_views inside of the courseware look like this...
            # event_type: [server] /courses/HarvardX/ER22x/2013_Spring/courseware/9158300eee2e4eb7a51d5a01ee01afdd/c2dfcb30d6d2490e85b83f882544fb0f/
            v = "page_view"
            path = event_type.split("courseware")[1]
            if(path[-1] == "/"): path = path[:-1]
            try: o_name = self.axis_path_to_courseware_name[path]
            except KeyError: return None # page is noise b/c not in axis
            o = {
                "object_type" : "courseware_name",
                "object_name" : o_name
            }
            r = None
            m = None
        elif(re_page_view_main.search(event_type)):
            # page_views outside of the courseware (top-level tabs) look like this...
            # event_type: [server] /courses/HarvardX/CB22x/2013_Spring/info
            v = "page_view"
            last_item = event_type.split("/")[-1]
            if(last_item == ""): # sometimes has trailing slash
                last_item = event_type.split("/")[-2]
            try: o_name = top_level_tabs[last_item]
            except KeyError: return None # if not in our list of tabs, must be noise
            o = {
                "object_type" : "tab_name",
                "object_name" : o_name
            }
            r = None
            m = None
        elif(re_page_close.search(event_type)):
            # TODO: how reliable are page_close events within edX and across browsers?
            # page: https://courses.edx.org/courses/HarvardX/CB22x/2013_Spring/courseware/74a6ab26887c474eae8a8632600d9618/7b1ef88acd3743eb922d82781a2371cc/
            v = "page_close"
            try: path = page.split("courseware")[1]
            except IndexError:
                # print "page_close IndexError: " + page
                return None # usually: https://courses.edx.org/courses/HarvardX/ER22x/2013_Spring/discussion/forum
            if(len(path) > 0 and path[-1] == "/"): path = path[:-1]
            try: o_name = self.axis_path_to_courseware_name[path]
            except KeyError: return None # page is noise b/c not in axis
            o = {
                "object_type" : "courseware_name",
                "object_name" : o_name
            }
            r = None
            m = None
            
        else:
            return None

        if(v == "page_view" and o_name == None): return None

        # unicode is the worst
        try: o.update((k, v.encode('utf8', 'replace')) for k, v in o.items())
        except Exception: pass # NoneType
        activity = {
            "actor": log_item_json["username"]
            ,"verb": v
            ,"object": o
            ,"result": r
            ,"meta": m
            ,"time": log_item_json["time"]
            ,"ip": log_item_json["ip"]
            ,"event": event
            ,"event_type": event_type
            ,"page": page
            ,"agent": log_item_json["agent"]
        }
        for k, v in activity.items():
            try: activity[k] = v.encode('utf8', 'replace')
            except Exception: pass # NoneType
        return activity

    def __getHashPath(self, s):
        return "/".join(re_hash.findall(s)).encode("utf-8")

    def __getForumObject(self, event_type):
        # just returning raw hashes for now
        # TODO: how can we return something human-readable?
        o = {
            "object_type" : "forum_hash",
            "object_name" : self.__getHashPath(event_type)
        }
        return o

    def __getCoursewareObject(self, url_name):
        # courseware_name format is {chapter}/{sequential}/{vertical}/{resource}
        try: o_name = self.axis_url_name_to_courseware_name[url_name]
        except KeyError: o_name = "[Axis Lookup Failed: " + url_name + "]"
        o = {
            "object_type" : "courseware_name",
            "object_name" : o_name
        }
        return o