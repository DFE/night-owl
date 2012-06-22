# -*- coding: utf-8 -*-
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

TASK_START = "ONSTART"

TYPE_NOTE = "NOTE"
TYPE_WARNING = "WARNING"
TYPE_ERROR = "ERROR"
TYPE_IGNORED = "IGNORED"
TYPE_WARN_COUNT = "WARN_COUNT"
TYPE_ERROR_COUNT = "ERR_COUNT"

START_STATE_ERRORLOGGER = ("["+TASK_START+"]",False,0,0)
