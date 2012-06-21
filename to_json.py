#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Open Embedded Under Control - the Continuous Integration and Controlling platform for OpenEmbedded Projects
# OEUC error-log - a framework for logging and presentation of errors and warnings
#
# Copyright (C) 2012 DResearch Fahrzeugelektronik GmbH
# Written and maintained by Thilo Fromm <fromm@dresearch-fe.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.
#
from __future__ import print_function

import sys
import argparse
import re
import json

from constants import *


def make_notification(job_name,build_num,notif_type, task_name, message):
    """create a notification dict (e.g. error or warning)

    :param job_name: how you want your build-task to be called (e.g. the name of your Jenkins Job)
    :param build_num: only meaningful if you have a Continious Integration tool running
    :param notif_type: what kind of notification it is. have a look in constants.py
    :param task_name: what bitbake task was running when this notification was generated
    :param message: the content of the notification
    :return: a dict with all params of this function
    """
    return {'job':job_name,'build':build_num,'type':notif_type,'task':task_name,'message':message}

def make_count(job_name,build_num,notif_type,count):
    """create a count dict

    :param job_name: how you want your build-task to be called (e.g. the name of your Jenkins Job)
    :param build_num: only meaningful if you have a Continious Integration tool running
    :param notif_type: what kind of notification it is. have a look in constants.py
    :param count: a number
    :return: a dict with all noteworthy information for a build-global counter
    """
    return {'job':job_name,'build':build_num,'type':notif_type,'count':count}

def parse_line(txt,job_name,build_num,task_name):
    """parse a line of error-log

    :param txt: the line that should be parsed
    :param job_name: how you want your build-task to be called (e.g. the name of your Jenkins Job)
    :param build_num: only meaningful if you have a Continious Integration tool running
    :param task_name: what bitbake task was running when this notification was generated
    :return: a make_notification() or make_count() result
    """
    out = ""
    if txt.startswith("WARNING:"):
        if not all([job_name,build_num,task_name]):
            raise Exception("Parse Error: Either job_name({0}),build_num({1}) or task_name({2}) was missing!".format(job_name,build_num,task_name))
        msg = re.sub(r'WARNING: ','',txt)
        out = json.dumps(make_notification(job_name,build_num, TYPE_WARNING,task_name,msg),sort_keys=True)
    elif txt.startswith("ERROR:"):
        if not all([job_name,build_num,task_name]):
            raise Exception("Parse Error: Either job_name({0}),build_num({1}) or task_name({2}) was missing!".format(job_name,build_num,task_name))
        msg = re.sub(r'ERROR: ','',txt)
        out = json.dumps(make_notification(job_name,build_num, TYPE_ERROR,task_name,msg),sort_keys=True)
    elif re.search('count',txt):
        type_name = TYPE_ERROR_COUNT if re.search(r'error',txt,flags=re.I) else TYPE_WARN_COUNT
        count = txt.split(':')[1].strip()
        out = json.dumps(make_count(job_name,build_num,type_name,int(count)),sort_keys=True)
    return out

def parse_errorlog(instream,job_name=None,build_num=None,task_name=None,mprint=None):
    """take an error-log per instream and parse it to json
    :param instream: the inputstream (or a simple list with each 'line' as a seperated element)
    :param job_name: how you want your build-task to be called (e.g. the name of your Jenkins Job)
    :param build_num: only meaningful if you have a Continious Integration tool running
    :param task_name: what bitbake task was running when this notification was generated
    :param mprint: the print function. shouldn't be touched and is just parameterized for unittests
    """
    if not mprint: mprint=print
    for line in instream:
        txt = line.strip()
        if txt.startswith("---"):
            #remove unnessesary characters
            build_msg = re.sub(r'(--*)|\[|\]','',txt).split(':')[1]
            job_name, build_num = build_msg[:-1].split('(')
        elif txt.startswith("["):
            task_name = txt[1:-1]
        elif len(txt) == 0:
            pass
        else:
            mprint(parse_line(txt,job_name,int(build_num),task_name))


def main():
    parser = argparse.ArgumentParser(
               description="reads error_log and generates database-style json")
    args = parser.parse_args()
    parse_errorlog(sys.stdin)

if __name__ == '__main__':
    main()
