#!/usr/bin/python2 -tt
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

from graph import Graph

class IgnoredWarning(Warning);
    "is raised, when elements in a sequence are ignored"
    pass

class Diagram(object):
    """
    can read json from an input stream and create pylab graphs from it.
    The resulting diagram will be JPEG file containing a title, a named x-axis,
    a named y-axis on the left showing the number of warnings, a named y-axis
    on the right showing the number of errors and 2 graphs, for warnings and
    errors separated.
    """

    DEFAULT_FILENAME="plot.png"
    DEFAULT_TITLE="Diagram"
    DEFAULT_GRAPH_LIST = []

    def __init__(self, filename=None, title=None,all_graphs=None):
        """
        :param filename: is the location, where the graph JPEG should be stored
        :param title: is the graph title that is written above the diagram
        """
        self.filename = filename if filename else Diagram.EFAULT_FILENAME
        self.title = title if title else Diagram.DEFAULT_TITLE
        self.all_graphs = all_graphs if all_graphs else DEFAULT_GRAPH_LIST


    def draw(self):
        """
        draws the graph with help of pylab. All values are taken from
        Object attributes, so there is neither input nor output needed.
        """
        plots = []
        for element in all_graphs:
            if isinstance(element,tuple):
                if len(element) != 2:
                    raise IgnoredWarning("expected a tuple of size 2.\n"\
                            + "More graphs in one diagram isn't meaningful. "\
                            + "Ignored '{}'".format(element))
                    continue
                if not all((isinstance(e,Graph) for e in element)):
                    raise IgnoredWarning("both elements should be element of "\
                            + "Graph. Ignored '{}'".format(element))
                    continue
                both = element # improving readability
                plot1 = plt.figure().add_subplot(111)
                plots.append(plot1)
                self.__init_plot(plot1)
                plot2 = plot1.twinx()
                plots.add(plot2)
                self.__init_plot(plot2)

            elif isinstance(element, Graph):
                single = element #improve readability
                plot = plt.figure().add_subplot(111)
                plots.append(plot)
                self.__init_plot(plot)

            else:
                raise IgnoredWarning("expect ellements to be tuple or Graph,"\
                        + "but found '{}'".format(element))
                continue
        plt.title(self.title)
        plt.savefig(self.filename)

        def __init_plot(self,plot,graph):
                plot.set_xlabel(graph.xlabel)
                plot.set_ylabel(graph.ylabel)
                plot.plot(graph.xdata, graph.ydata,graph.formatting,
                        label=graph.name)
                plot.axis([0,graph.xdata.max()*1.1,
                            0,graph.ydata.max()*1.1)



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
