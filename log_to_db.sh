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
USAGE="usage: log_to_db.sh <log_file> <db_name>"

if [ -z $1 ]; then
    echo "$USAGE"
    exit 1
fi

if [ -z $2 ]; then
    echo "$USAGE"
    exit 1
fi

#check if table needs to be created
table_exists=$(sqlite3 $2 ".schema signal")
if [ -z "$table_exists" ]; then
    echo "init db: $2"
    ./init_db.sh $2 >/dev/null #silence
fi

echo "start parsing..."
cat $1 \
    | ./parse_signals.py \
    | sed "s/^(/&NULL,/" \
    | sed "s/)$/, datetime('now')&/" \
    | sed 's/.*/INSERT INTO signal VALUES&;/' \
    | sqlite3 $2
echo "Done."
