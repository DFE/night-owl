#!/bin/sh
# -*- coding:utf-8 -*-
#
# Open Embedded Under Control - the Continuous Integration and Controlling platform for OpenEmbedded Projects
# OEUC error-log - a framework for logging and presentation of errors and warnings
#
# Copyright (C) 2012 DResearch Fahrzeugelektronik GmbH
# Written and maintained by Erik Bernoth <bernoth@dresearch-fe.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.
#

test/tools/generate_warnings.py 130 200 | ./filter_errorlog.py testA 1 
test/tools/generate_warnings.py 120 200 | ./filter_errorlog.py testA 2 
test/tools/generate_warnings.py 110 200 | ./filter_errorlog.py testA 3 
test/tools/generate_warnings.py 100 200 | ./filter_errorlog.py testA 4 
test/tools/generate_warnings.py 100 200 | ./filter_errorlog.py testA 5 

test/tools/generate_warnings.py 190 200 | ./filter_errorlog.py testB 1 
test/tools/generate_warnings.py 170 200 | ./filter_errorlog.py testB 2 
test/tools/generate_warnings.py 110 200 | ./filter_errorlog.py testB 3 
test/tools/generate_warnings.py 30 200 | ./filter_errorlog.py testB 4
test/tools/generate_warnings.py 10 200 | ./filter_errorlog.py testB 5 

test/tools/generate_warnings.py 150 200 | ./filter_errorlog.py testC 1 
test/tools/generate_warnings.py 150 200 | ./filter_errorlog.py testC 2 
test/tools/generate_warnings.py 150 200 | ./filter_errorlog.py testC 3 
test/tools/generate_warnings.py 140 200 | ./filter_errorlog.py testC 4 
test/tools/generate_warnings.py 130 200 | ./filter_errorlog.py testC 5 
