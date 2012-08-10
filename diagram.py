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

""" draws graphs from json strings """

from __future__ import print_function

import sys
import re
import argparse
import json

import numpy as np
import matplotlib
#nessesary here for generating output without a window object
matplotlib.use('AGG') 
import matplotlib.pyplot as plt

from constants import *


class Diagram(object):
    """
    can read json from an input stream and create pylab graphs from it.
    The resulting diagram will be JPEG file containing a title, a named x-axis,
    a named y-axis on the left showing the number of warnings, a named y-axis
    on the right showing the number of errors and 2 graphs, for warnings and
    errors separated.
    """


    def __make_msgline(self,x=None,y=None):
        """creates a touple that will be used for drawing diagrams

        TODO: rewrite functionality

        :param x: a numpy array
        :param y: a numpy array
        :return: a 'msgline'
        """
        if not x: x = np.array([])
        if not y: y = np.array([])
        return (x,y)


    def __append_msgline(self,msgline,px,py):
        """helper function for adding stuff to an object generated by make_msgline()

        TODO: rewrite functionality

        :param msgline: a touple as returned by make_msgline() or append_msgline()
        :param px: a new x-value to add
        :param py: a new y-value to add
        :return: a 'msgline'
        """
        return (np.concatenate((msgline[0],np.array([px]))),
                np.concatenate((msgline[1],np.array([py]))))


    def __init__(self, warnings=None, errors=None, filename=None, title=None,
            xlabel=None, ylabel_warn=None, ylabel_err=None, format_warn=None,
            format_err=None):
        """create a new Diagram.

        :param warnings: is a list of integers, containing number of warnings 
                         per build
        :param errors: is a list of integers, containing number of errors 
                       per build
        :param filename: is the location, where the graph JPEG should be stored
        :param title: is the graph title that is written above the diagram
        :param xlabel: names the x-axis on the diagram
        :param ylabel_warn: names the y-axis for warnings.
        :param ylabel_err: names the y-axis for errors.
        :param format_warn: Matlab style formatting of the warning graph
        :param format_err: Matlab style formatting of the error graph
        """
        self.warnings = warnings if warnings else self.__make_msgline()
        self.errors = errors if errors else self.__make_msgline()
        self.filename = filename if filename else ""
        self.title = title if title else ""
        self.xlabel = xlabel if xlabel else ""
        self.ylabel_warn = ylabel_warn if ylabel_warn else ""
        self.ylabel_err = ylabel_err if ylabel_err else ""
        self.format_warn = format_warn if format_warn else ""
        self.format_err = format_err if format_err else ""


    def parse_input(self, instream):
        """parses data from an inputstream gracefully,
        i.e. parses input that it understands and ignores everything else.

        :param instream: an inputstream, like sys.stdin
        :return: warnings, errors (both lists of lists of numbers)
        """
        for line in instream:
            try:
                counter = json.loads(line)
            except ValueError:
                continue
            x_warn = x_err = counter['attempt'] if 'attempt' in counter else -1
            y_warn = counter['warnings'] if 'warnings' in counter else 0
            y_err = counter['errors'] if 'errors' in counter else 0
            self.warnings = self.__append_msgline(self.warnings,x_warn,y_warn)
            self.errors = self.__append_msgline(self.errors, x_warn, y_warn)
        return self.warnings, self.errors


    def draw(self):
        """draws the graph with help of pylab. All values are taken from
        Object attributes, so there is neither input nor output needed.
        """
        warn_plot = plt.figure().add_subplot(111)
        warn_plot.set_xlabel(self.xlabel)
        warn_plot.set_ylabel(self.ylabel_warn)

        warn_plot.plot(self.warnings[0],self.warnings[1],self.format_warn, 
                label="Warnings")
        warn_plot.axis([0, self.warnings[0].max()*1.1, 0, 
            self.warnings[1].max()*1.1])

        err_plot = warn_plot.twinx()
        err_plot.set_xlabel(self.xlabel)
        err_plot.set_ylabel(self.ylabel_err)
        err_plot.plot(self.errors[0],self.errors[1],self.format_err,label="Errors")
        err_plot.axis([0, self.errors[0].max()*1.15, 0, self.errors[1].max()*1.15])

        plt.title(self.title)
        plt.savefig(self.filename)


def set_from_cli(user=None):
    """handles the values given when used by it's CLI and sets attributes of an
    optional object accordingly.

    :param user: gets it's values set according to the parsed args.
    :return: returns the parsed args for further usage.
    """
    parser = argparse.ArgumentParser(
            description="generates graphs from error-json lines")
    parser.add_argument("filename", nargs="?", default="plot",
            type=str, help="name of the picture-file")
    parser.add_argument("title",nargs="?",default="plot",type=str,
            help="the written title over the plot")
    parser.add_argument("xlabel",nargs="?",
            default="build no.", type=str, help="label for x-axis")
    parser.add_argument("ylabel_warn",nargs="?",
            default="No. of Warnings", type=str,
            help="label for left y-axis, i.e. warnings")
    parser.add_argument("ylabel_err",nargs="?",default="No. of Errors",
            type=str, help="label for right y-axis, i.e. errors")
    parser.add_argument("format_warn",nargs="?",type=str,default="g--",
            help="Matlab formatting for the warnings")
    parser.add_argument("format_err",nargs="?",type=str,default="r-o",
            help="Matlab formatting for the errors")
    args = parser.parse_args()
    if user:
        user.filename = args.filename
        user.title = args.title
        user.xlabel = args.xlabel
        user.ylabel_warn = args.ylabel_warn
        user.ylabel_err = args.ylabel_err
        user.format_warn = args.format_warn
        user.format_err = args.format_err
    return args

def main():
    diagram = Diagram()
    set_from_cli(diagram)
    diagram.parse_input(sys.stdin)
    diagram.draw()


if __name__ == '__main__':
    main()