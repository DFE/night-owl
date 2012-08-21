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

import sys
import argparse

import framework as fw

class NightOwl(object):
    """
    is the manager class for the night-owl module.
    """

    DEFAULT_FILENAME = "night-owl.png"
    DEFAULT_TITLE = "Night Owl Errors/Warnings"
    DEFAULT_XLABEL = "Build Number"
    DEFAULT_YLABEL_WARNG = "Warnings/Build"
    DEFAULT_YLABEL_ERROR = "Errors/Build"
    DEFAULT_FORMAT_WARNG = "g--"
    DEFAULT_FORMAT_ERROR = "r-o"


    def __init__(self, filename=None, title=None, xlabel=None,
            ylabel_warng=None, ylabel_error=None, format_warng=None,
            format_error=None):
        self.filename = filename if filename is not None \
                                                else self.DEFAULT_FILENAME
        self.title = title if title is not None else self.DEFAULT_TITLE
        self.xlabel = xlabel if xlabel is not None else self.DEFAULT_XLABEL
        self.ylabel_warng = ylabel_warng if ylabel_warng is not None \
                                                else self.DEFAULT_YLABEL_WARNG
        self.ylabel_error = ylabel_error if ylabel_error is not None \
                                                else self.DEFAULT_YLABEL_ERROR
        self.format_warng = format_warng if format_warng is not None \
                                                else self.DEFAULT_FORMAT_WARNG
        self.format_error = format_error if format_error is not None \
                                                else self.DEFAULT_FORMAT_ERROR


    def read_json(self,input_):
        """
        creates a generator expression for reading json from standard input.

        :param input_: an interable or a single line of JSON txt
        :return: a generator expression of :py:class:framework.Signal objects
        """
        self.signals = fw.Signal.make_from_json(input_)


    def draw_warning_error_graph(self):
        """
        draws a diagram of an :py:class:collections.Iterable of Signal objects
        """
        warnings = fw.Graph(fw.Graph.TYPE_WARNING, self.xlabel,
                self.ylabel_warng, self.format_warng)
        errors = fw.Graph(fw.Graph.TYPE_ERROR, self.xlabel,
                self.ylabel_error, self.format_error)
        add = {
                fw.Signal.TYPE_WARNING : warnings.add_signals,
                fw.Signal.TYPE_ERROR : errors.add_signals
        }
        for signal in self.signals:
            if not hasattr(signal,"type_"):
                continue
            add[signal.type_](signal)

        self.diagram = fw.Diagram(filename=None,title=None,
                all_graphs=((warnings,errors),))
        self.diagram.draw()



def main():
    parser = argparse.ArgumentParser(
               description="generates graphs from error-json lines")
    parser.add_argument("filename",nargs="?",default=NightOwl.DEFAULT_FILENAME,
                            type=str, help="name of the picture-file")
    parser.add_argument("title",nargs="?",default=NightOwl.DEFAULT_TITLE,
                            type=str, help="the written title over the plot")
    parser.add_argument("xlabel",nargs="?",default=NightOwl.DEFAULT_XLABEL,
                            type=str, help="label for x-axis")
    parser.add_argument("ylabel_warn",nargs="?",
                            default=NightOwl.DEFAULT_YLABEL_WARNG, type=str,
                            help="label for left y-axis, i.e. warnings")
    parser.add_argument("ylabel_err",nargs="?",
                            default=NightOwl.DEFAULT_YLABEL_ERROR, type=str,
                            help="label for right y-axis, i.e. errors")
    parser.add_argument("format_warn",nargs="?",type=str,
                            default=NightOwl.DEFAULT_FORMAT_WARNG,
                            help="Matlab formatting for the warnings")
    parser.add_argument("format_err",nargs="?",type=str,
                            default=NightOwl.DEFAULT_FORMAT_ERROR,
                            help="Matlab formatting for the errors")
    args = parser.parse_args()
    night_owl = NightOwl(
            args.filename,
            args.title,
            args.xlabel,
            args.ylabel_warn,
            args.ylabel_err,
            args.format_warn,
            args.format_err,
    )
    night_owl.read_json(sys.stdin)
    night_owl.draw_warning_error_graph()



if __name__ == "__main__":
    main()
