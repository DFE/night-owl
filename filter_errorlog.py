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
import re
import argparse

def main():
    parser = argparse.ArgumentParser(description="creates error-logs \
                                                 from bitbake log input")
    parser.add_argument("job", type=str, nargs="?",default="UNKNOWN",help="the name of the job the build belongs to")
    parser.add_argument("build",type=int,nargs="?",default="-1",help="the number of the build")
    args = parser.parse_args()

    task_name = "ONSTART"
    task_printed = False
    warning_count = 0
    error_count = 0


    print "----------[START:{0}({1})]----------".format(args.job,args.build)
    for line in sys.stdin:
        if line.startswith("NOTE: package"):
            task_name = re.sub(r'NOTE: package (.*)',r'\1',line,re.I)
            task_name = re.sub(r'(: Started\s*)|(: Succeeded\s*)|(: Failed\s*)',r'',task_name,re.I)
            task_printed = False
        elif re.match(r'^warning:', line,re.I):
            warning_count += 1
            if not task_printed:
                print "\n[{0}]".format(task_name)
                task_printed = True
            print re.sub(r'^warning:','WARNING:',line,flags=re.I),
        elif re.match(r'^error:', line,re.I):
            error_count += 1
            if not task_printed:
                print "\n[{0}]".format(task_name)
                task_printed = True
            print re.sub(r'^error:','ERROR:',line,flags=re.I),
    print "\n\nWarning count: {0}".format(warning_count)
    print "Error count: {0}".format(error_count)
    print "----------[END:{0}({1})]----------".format(args.job,args.build)


if __name__ == "__main__":
    main()
