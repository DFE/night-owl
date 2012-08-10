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
manages everything that is related to one single message,
e.g. a warning from bitbake or an error for make
"""

from __future__ import print_function

import sys
import re
import argparse
import json

from constants import *

class Signal(object):
    """
    is a single message like an error or a warning plus it's additional
    information. 
    """

    def __init__(self,signal_tid=None,type_=None,attempt=None,msg=None
            cat=None,recipe=None,cmd=None,file_=None,row=None,col=None,
            time=None):
        self.signal_tid = signal_tid if signal_tid else -1
        self.type_ = type_ if type_ else ""
        self.attempt = attempt if attempt else -1
        self.msg = msg if msg else ""
        self.cat = cat if cat else ""
        self.recipe = recipe if recipe else ""
        self.cmd = cmd if cmd else ""
        self.file_ = file_ if file_ else ""
        self.row = row if row else -1
        self.col = col if col else -1
        self.time = time if time else ""

def make_signal_from_json(txt):
    """
    is a factory function to parse directly from json
    :param txt: is a :py:class:Signal as a valid json string
    :return: :py:class:Signal object
    """
    json_ = json.loads(txt)
    return Signal(
            json_.signal_tid,
            json_.type,
            json_.attempt,
            json_.msg,
            json_.cat,
            json_.recipe,
            json_.cmd,
            json_.file,
            json_.row,
            json_.col,
            json_.time,
    )


def make_many(instream):
    """
    can be used to parse an input stream like sys.stdin for signal like json
    strings.

    :param instream: an input stream or iterator of strings
    :return: a generator for many json objects
    """
    return (make_signal_from_json(line) for line in instream)
