#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# NightOwl - who tests your unit tests?
#
# Copyright (C) 2012 DResearch Fahrzeugelektronik GmbH
# Written and maintained by Erik Bernoth <bernoth@dresearch-fe.de>
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
import copy
import inspect
from constants import *

def make_signal(sig_type, attempt, msg, cat, recipe, cmd, prob_file, row, col):
    """create a tuple of attributes in signal table form"""
    return (sig_type, attempt, msg, cat, recipe, cmd, prob_file, row, col)


def filter_lines(instream,filters):
    """ignore lines that are not needed
    :param instream: an input stream to read data from
    :param filters: a list of compiled regexes
    :yield: a tupel (line, regex)
    """
    for line in instream:
        for regex in filters:
            if regex.match(line):
                yield (line,regex)
                break

def parse_line(line, regex,reg_to_type,state=copy.deepcopy(STATE_PARSER_START)):
    if reg_to_type[regex] == TYPE_NOTE:
        state['recipe'], state['cmd'] = regex.findall(line)[0]
        return Null
    elif reg_to_type[regex] in (TYPE_WARNING,TYPE_ERROR):
        return make_signal(
                sig_type=reg_to_type[regex],
                attempt=DEFAULT_SIG_ATTEMPT,
                msg=re.sub(r'"',"'",regex.findall(line)[0]),
                cat=DEFAULT_SIG_CATEGORY,
                recipe=state['recipe'],
                cmd=state['cmd'],
                prob_file=DEFAULT_SIG_FILE,
                row=DEFAULT_SIG_ROW,
                col=DEFAULT_SIG_COL,
        )

def filtered_print(txt):
    """prints only if txt is not None and also enables logging"""
    print(txt) if txt else None #note that this requires print being a function

def main(mprint=filtered_print):
    filters = [
        re.compile("NOTE: ([^:]+):([^ ]+).*",re.I),
        re.compile("ERROR: (.+)",re.I),
        re.compile("WARNING: (.+)",re.I)
    ]
    #translate regex objects to type-tags
    reg_to_type = {
            filters[0] : TYPE_NOTE,
            filters[1] : TYPE_ERROR,
            filters[2] : TYPE_WARNING
    }
    for line,regex in filter_lines(sys.stdin, filters):
        signal = parse_line(line,regex,reg_to_type)
        mprint(signal)

if __name__ == '__main__':
    main()
