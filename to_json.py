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
    """
    return {'job':job_name,'build':build_num,'type':notif_type,'count':count}

def main():
    parser = argparse.ArgumentParser(
               description="reads error_log and generates database-style json")
    args = parser.parse_args()
    job_name = None
    build_num = None
    task_name = None
    for line in sys.stdin:
        line = line.strip()
        if line.startswith("---"):
            #remove unnessesary characters
            build_msg = re.sub(r'(--*)|\[|\]','',line).split(':')[1]
            job_name, build_num = build_msg[:-1].split('(')
        elif line.startswith("["):
            task_name = line[1:-1]
        elif line.startswith("WARNING:"):
            if not all([job_name,build_num,task_name]):
                raise Error("Parse Error: Either job_name({0}),build_num({1}) or task_name({2}) was missing!".format(job_name,build_num,task_name))
            msg = re.sub(r'WARNING:','',line)
            print json.dumps(make_notification(job_name,build_num, TYPE_WARNING,task_name,msg),sort_keys=True)
        elif line.startswith("ERROR:"):
            if not all([job_name,build_num,task_name]):
                raise Error("Parse Error: Either job_name({0}),build_num({1}) or task_name({2}) was missing!".format(job_name,build_num,task_name))
            msg = re.sub(r'ERROR:','',line)
            print json.dumps(make_notification(job_name,build_num, TYPE_ERROR,task_name,msg),sort_keys=True)
        elif re.search('count',line):
            type_name = TYPE_ERROR if re.search(r'error',line,flags=re.I) else TYPE_WARNING
            count = line.split(':')[1].strip()
            print json.dumps(make_count(job_name,build_num,type_name,count),sort_keys=True)




if __name__ == '__main__':
    main()
