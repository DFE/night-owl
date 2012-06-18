#!/bin/sh
# -*- coding:utf-8 -*-
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

./generate_warnings.py 130 200 | ./log_errors.py testA 0 
./generate_warnings.py 120 200 | ./log_errors.py testA 1 
./generate_warnings.py 110 200 | ./log_errors.py testA 2 
./generate_warnings.py 100 200 | ./log_errors.py testA 3 
./generate_warnings.py 100 200 | ./log_errors.py testA 4 

./generate_warnings.py 190 200 | ./log_errors.py testB 0 
./generate_warnings.py 170 200 | ./log_errors.py testB 1 
./generate_warnings.py 110 200 | ./log_errors.py testB 2 
./generate_warnings.py 30 200 | ./log_errors.py testB 3 
./generate_warnings.py 10 200 | ./log_errors.py testB 4 

./generate_warnings.py 150 200 | ./log_errors.py testC 0 
./generate_warnings.py 150 200 | ./log_errors.py testC 1 
./generate_warnings.py 150 200 | ./log_errors.py testC 2 
./generate_warnings.py 140 200 | ./log_errors.py testC 3 
./generate_warnings.py 130 200 | ./log_errors.py testC 4 
