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
import re
import argparse
from constants import *

def parse_line(line):
    """reads and translates one line of bitbake log

    :param line: the line of bitbake log
    :return: a touple of (output-txt, token_type)
    """
    out = ""
    token_type = TASK_START
    if line.startswith("NOTE: package"):
        task_name = re.sub(r'NOTE: package (.*)',r'\1',line,re.I)
        task_name = re.sub(r'(: Started\s*)|(: Succeeded\s*)|(: Failed\s*)',
                           r'',task_name,re.I)
        out += "[{0}]".format(task_name)
        token_type = TYPE_NOTE
    elif re.match(r'^warning:', line,re.I):
        token_type = TYPE_WARNING
        sub = re.sub(r'^warning:','WARNING:',line,flags=re.I)
        out += sub
    elif re.match(r'^error:', line,re.I):
        token_type = TYPE_ERROR
        out += re.sub(r'^error:','ERROR:',line,flags=re.I)
    else:
        token_type = TYPE_IGNORED
    ret_val = (out,token_type)
    return (out,token_type)


def parse_build(job,build,instream,start_state=None,mprint=print):
    if not start_state: start_state = START_STATE_ERRORLOGGER
    task,task_printed,warning_count, error_count = start_state

    mprint("----------[START:{0}({1})]----------".format(job,build))
    for line in instream:
        token = parse_line(re.sub(r'\n','',line))
        txt = token[0]
        if token[1] == TYPE_WARNING:
            warning_count+=1
        elif token[1] == TYPE_ERROR:
            error_count+=1
        if txt.startswith("["):
            task = txt
            task_printed = False
        else:
            if not task_printed:
                task_printed = True
                mprint()
                mprint(task)
            mprint(txt)

    mprint()
    mprint()
    mprint("Warning count: {0}".format(warning_count))
    mprint("Error count: {0}".format(error_count))
    mprint()
    mprint("----------[END:{0}({1})]----------".format(job,build))

def main():
    parser = argparse.ArgumentParser(description="creates error-logs \
                                                 from bitbake log input")
    parser.add_argument("job", type=str, nargs="?",default="UNKNOWN",
                        help="the name of the job the build belongs to")
    parser.add_argument("build",type=int,nargs="?",default="-1",
                        help="the number of the build")
    args = parser.parse_args()


    parse_build(args.job,args.build,sys.stdin)




if __name__ == "__main__":
    main()
