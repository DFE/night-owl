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
import json

from constants import *

def new_count():
    return {'warnings':0,'errors':0,'attempt':-1}

def count(instream,mprint=print):
    state = {}
    for line in instream:
        signal = json.loads(line)
        attempt = signal['attempt']
        if not attempt in state:
            state[attempt] = new_count()
            state[attempt]['attempt']=attempt
        freq = 'warnings' if signal['type'] == TYPE_WARNING else 'errors'
        state[attempt][freq] += 1
    for count in state.values():
        mprint(json.dumps(count))

def main():
    count(sys.stdin)

if __name__ == '__main__':
    main()
