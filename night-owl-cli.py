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
contains everything related to the user interface for night-owl.
"""

from __future__ import print_function

import framework as fw

class NightOwl(object):
    """
    is the manager class for the night-owl module.
    """

    DEFAULT_FILENAME = "night-owl.png"
    DEFAULT_TITLE = "Night Owl Errors/Warnings"

    TYPE_WARNING = "WARNING"
    TYPE_ERROR = "ERROR"

    def __init__(self):
        pass


    def read_json(input_):
        """
        creates a generator expression for reading json from standard input.

        :param input_: an interable or a single line of JSON txt
        :return: a generator expression of :py:class:framework.Signal objects
        """
        return fw.Signal.make_from_json(input_)


    def draw_warning_error_graph(signals):
        """
        draws a diagram of an :py:class:collections.Iterable of Signal objects
        """
        accumulators = fw.SignalAccumulator.make_many(signals)
        warning_accums = (accumulators[k] for k in keys
                        if accumulators[k].type_ = TYPE_WARNING)
        error_accums = (accumulators[k] for k in keys
                        if accumulators[k].type_ = TYPE_ERRORS)




if __name__ == "__main__":
    read_json(sys.stdin,(fw.Signal.TYPE_WARNING,fw.Signal.TYPE_ERROR))
