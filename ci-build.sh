#!/bin/bash
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



#-----------------------------------
# preparations
#-----------------------------------

#this is how Jenkins should recognise the results as artifacts
#don't change that, if u are not familiar with Jenkins' artifacts
PRE=nightowl 

#the name of the error-log File. Leave the $PRE in the beginning
ERROR_LOG=$PRE-error.log

#name of the graphi-file.
#Leave the $PRE in the beginning and no file ending needed
GRAPH_FILE=$PRE-error

#name written on top of the plot
GRAPH_NAME=Errors/Warnings\ per\ Build

#name of the x-axis
LABEL_X=Build\ no.

#name of the y-axis
LABEL_Y=No.\ of\ Errors/Warnings

#format string
FORMAT_WARNINGS=g--

#format string
FORMAT_ERRORS=r-o

#-----------------------------------
# here begins the action
#-----------------------------------
cat $1/log | ./filter_errorlog.py >>$ERROR_LOG
cat $ERROR_LOG | ./to_json.py | grep count | ./to_graph.py $ERROR_GRAPH
