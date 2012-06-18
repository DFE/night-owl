#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Open Embedded Under Control - the Continuous Integration and Controlling platform for OpenEmbedded Projects
# OEUC error-log - a framework for logging and presentation of errors and warnings
#
# Copyright (C) 2012 DResearch Fahrzeugelektronik GmbH
# Written and maintained by Thilo Fromm <fromm@dresearch-fe.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.
#

import sys
import re
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt

from constants import *


def make_msgline(x=None,y=None):
    """creates a touple that will be used for drawing diagrams

    :param x: a numpy array
    :param y: a numpy array
    :return: a 'msgline'
    """
    if not x: x = np.array([])
    if not y: y = np.array([])
    return (x,y)


def append_msgline(msgline,px,py):
    """helper function for adding stuff to an object generated by make_msgline()

    :param msgline: a touple as returned by make_msgline() or append_msgline()
    :param px: a new x-value to add
    :param py: a new y-value to add
    :return: a 'msgline'
    """
    return (np.concatenate((msgline[0],np.array([px]))),
            np.concatenate((msgline[1],np.array([py]))))

def main():
    parser = argparse.ArgumentParser(
               description="generates graphs from error-json lines")
    parser.add_argument("filename",nargs="?",default="plot",type=str,
                            help="name of the picture-file")
    parser.add_argument("title",nargs="?",default="plot",type=str,
                            help="the written title over the plot")
    parser.add_argument("xlabel",nargs="?",default="build no.",type=str,
                            help="label for x-axis")
    parser.add_argument("ylabel",nargs="?",default="No. of Errors/Warnings",
                            type=str,help="label for y-axis")
    parser.add_argument("format_warnings",nargs="?",type=str,default="g--",
                            help="Matlab formatting for the warnings")
    parser.add_argument("format_errors",nargs="?",type=str,default="r-o",
                            help="Matlab formatting for the errors")
    args = parser.parse_args()
    warnings = make_msgline()
    errors = make_msgline()

    #all this stuff just reads the json and tries to put it into a plot()
    for line in sys.stdin:
        msgjson = json.loads(line)
        if msgjson['type'] == TYPE_WARNING:
            warnings = append_msgline(warnings,warnings[0].size,float(msgjson['count']))
        elif msgjson['type'] == TYPE_ERROR:
            errors = append_msgline(errors,errors[0].size,float(msgjson['count']))
        else:
            raise Error("Strange type "+msgjson['type']+"!")
    plt.plot(warnings[0],warnings[1],args.format_warnings,label="Warnings")
    plt.plot(errors[0],errors[1],args.format_errors,label="Errors")
    plt.axis([0,max(warnings[0].max(),errors[0].max())*1.1,0,max(warnings[1].max(),errors[1].max())*1.1])
    plt.xlabel(args.xlabel)
    plt.ylabel(args.ylabel)
    plt.legend()
    plt.title(args.title)
    plt.savefig(args.filename)
    plt.show()


if __name__ == '__main__':
    main()
