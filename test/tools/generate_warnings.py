#!/usr/bin/python2
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

import random
import argparse

# a fill text for error messages
fill_txt = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
# pare string for fake package notifications
package_txt = "NOTE: package package_{0}: Started"

problem_choices = [
    "warning: ",
    "WARNING: ",
    "wArNiNG: ",
    "error: ",
    "Error: ",
    "ERROR: "
]

def generate_problem_line(txt=None,choices=None):
    """inserts a warning or error at the front of a txt message

    :param txt: the fill text, where the error/warning should be inserted
    :param choice: a list of things that could be inserted
    """
    if not txt: txt = fill_txt
    if not choices: choices = problem_choices
    out = random.choice(choices)+txt
    return out

def main():
    parser = argparse.ArgumentParser(description="generate messages with some \
                                     some of them containing warnings. \
                                     Choose the same value for min- and \
                                     max-values to get a specific \
                                     unrandomized result.")
    parser.add_argument("minwarn",type=int,
                        nargs="?",default=1,help="minimum number of warnings")
    parser.add_argument("mintasks",type=int,
                        nargs="?",default=1,help="minimum number of tasks")
    parser.add_argument("minout",type=int,
                        nargs="?",default=0,help="minimum number of lines")
    parser.add_argument("maxwarn",type=int,
                        nargs="?",default=1,help="maximum number of warnings")
    parser.add_argument("maxtasks",type=int,
                        nargs="?",default=1,help="maximum number of tasks")
    parser.add_argument("maxout",type=int,
                        nargs="?",default=0,help="maximum number of lines")
    args = parser.parse_args()

    #if user input contains min > max, errors will occur
    minwarn = args.minwarn
    maxwarn = args.maxwarn if args.maxwarn >= minwarn else minwarn
    minout = args.minout
    maxout = args.maxout if args.maxout >= minout else minout
    mintasks = args.mintasks
    maxtasks = args.maxtasks if args.maxtasks >= mintasks else mintasks
    
    warn_times = random.randint(minwarn,maxwarn)
    new_tasks = random.randint(mintasks,maxtasks)
    normal_times = random.randint(minout,maxout) - warn_times - new_tasks
    normal_times = normal_times if normal_times > 0 else 0
    lines = [txt for i in range(normal_times)] + \
            [package_txt.format(i+1) for i in range(new_tasks)]+\
            [generate_problem_line() for i in range(warn_times)]
    random.shuffle(lines)
    lines = [package_txt.format(0)]+lines
    print '\n'.join(lines)

if __name__ == "__main__":
    main()
