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
prepare data for presentation in a :py:class:diagram.Diagram
"""

from __future__ import print_function

import sys
import re
import argparse
import json

from constants import *

class Graph(object):
    """
    contains all data and information about a single graph inside a
    :py:class:diagram.Diagram.
    """

    def __init__(self,name, signal_accumulators, ylabel, formatting):
        """
        :param name: how the graph will be called in the diagram
        :param signal_accumulators: an iterator for signal_accumulators
        :param ylabel: naming of the corresponding y-axis in the diagram
        :param formatting: Matlab style formatting for this graph
        """
        self.name = name
        self.__signal_accumulators = signal_accumulators
        self.ylabel = ylabel
        self.formatting = formatting
        self.__xdata = np.array([])
        self.__ydata = np.array([])
        self.__applied = False

    def __apply_accumulators():
        """
        generate pylab parsable data from accumulators
        """
        self.__xdata = np.array([])
        self.__ydata = np.array([])
        for acc in self.signal_accumulators:
            self.__xdata = __array_append(self.__xdata,acc.attempt)
            self.__ydata = __array_append(self.__ydata,acc.count)
        self.__applied = True


    @property
    def signal_accumulators(self):
        return self.__signal_accumulators

    @signal_accumulators.setter
    def signal_accumulators(self,value):
        self.__signal_accumulators = value
        self.__applied = False

    @signal_accumulators.deleter
    def signal_accumulators(self):
        self.__signal_accumulators = None
        self.__applied = False

    @property
    def x_data(self):
        """
        generates data for the x values of a pylab graph plot
        """
        if not self.__applied:
            self.__apply_accumulators()
        return self.__xdata


    @property
    def y_data(self):
        """
        generates data for the y values of a pylab graph plot
        """
        if not self.__applied:
            self.__apply_accumulators()
        return self.__ydata


def __array_append(self, in_a,in_b):
    """
    append a numpy array to another
    :param in_a: a numpy array
    :param in_b: a numpy array or a number
    """
    in_b = np.array([in_b]) if isinstance(in_b,(int,float,long,complex)) else in_b
    return np.concatenate((in_a,in_b))
