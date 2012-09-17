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

"""
parses sqlite input and creates json from that
"""

from __future__ import print_function

import sys
import re
import json

def main():
    rin = re.compile("([^|]+)")
    keys = [
            "signal_tid",
            "type",
            "attempt",
            "msg",
            "cat",
            "recipe",
            "cmd",
            "file",
            "row",
            "col",
            "time"
    ]
    for line in sys.stdin:
        values = rin.findall(line)
        out = json.dumps(dict(zip(keys,values)))
        print(out)


if __name__ == "__main__":
    main()
