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

if [ -z $1 ]; then
    echo "usage: init_db.sh <db_name>"
    exit 1
fi

sqlite3 $1 "CREATE TABLE signal ( \
signal_tid INTEGER PRIMARY KEY, \
type TEXT, \
msg TEXT, \
cat TEXT, \
recipe TEXT, \
cmd TEXT, \
file TEXT, \
row INTEGER, \
col INTEGER \
);"

sqlite3 $1 ".schema signal"
