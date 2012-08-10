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
manages a group of like minded signals
"""

from __future__ import print_function

import sys
import re
import argparse
import json

from constants import *
class SignalIgnoredWarning(Warning):
    pass

class SignalAccumulator(object):
    """
    maintains a group of signals
    """

    def __init__(self, type_, attempt=None, count=None)
        self.type_ = type_
        self.attempt = attempt if attempt else -1
        self.count = count if count else 0

    def add_signal(self,signal):
        if signal.attempt != self.attempt:
            raise SignalIgnoredWarning("Attempt {} isn't mine ({}) -> ignored".format(
                                                    signal.attempt,
                                                    self.attempt
                                       ))
        else:
            self.count +=1
    
    def add_signals(self,signal_iterator):
        map(self.add_signal,signal_iterator)

def make_many(signal_iterator):
    """
    can be used, when you have a long list of signals of different attempts and
    you want to automatically create a list of :py:class:SignalAccumulator
    objects for each attempt.

    :param signal_iterator: should deliver :py:class:signal.Signal objects
    :return: a generator for all :py:class:SignalAccumulator objects
    """
    accumulators = {}
    for signal in signal_iterator:
        if signal.attempt not in accumulators:
            accumulators[signal.attempt] = SignalAccumulator(signal.attempt)
        accumulators[signal.attempt].add_signal(signal)
    keys = accumulators.keys()
    keys.sort()
    return (k, accumulators[k] for k in keys)
