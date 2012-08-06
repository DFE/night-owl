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

#Where this script lies. This is import for calling the other scripts
THIS=$(dirname $0)

#where the artifacts will be stored
RES_DIR="$THIS/../build/night-owl"
mkdir -p $RES_DIR

#where to find the build logs
BUILD_LOG=$(ls -1 $THIS/../build/tmp-eglibc/cooker.log.* | sort -n | tail -1)

#where the data is stored
DB_NAME="$THIS/../build/night-owl/logging.db"

#this is how Jenkins should recognise the results as artifacts
#don't change that, if u are not familiar with Jenkins' artifacts
PRE=$RES_DIR/night-owl 

#the name of the error-log File. Leave the $PRE in the beginning
ERROR_LOG=$PRE-error.log

# Name of the compiler warnigs per package log file
CC_WARNINGS_LOG=$PRE-cc-warn.log

#name of the graphi-file.
#Leave the $PRE in the beginning and no file ending needed
GRAPH_FILE=$PRE-error

#name written on top of the plot
GRAPH_NAME="Errors/Warnings per Build"

#name of the x-axis
LABEL_X="Build no."

#name of the left y-axis
LABEL_Y_LEFT="No. of Warnings"

#name of the right y-axis
LABEL_Y_RIGHT="No. of Errors"

#format string
FORMAT_WARNINGS=g--

#format string
FORMAT_ERRORS=r-o


#-----------------------------------
# here begins the action
#-----------------------------------

JOB="nightowl-job"
BUILD_NUM=$(date +%s)

[ $# -ge 1 ] && JOB="$1"
[ $# -ge 2 ] && BUILD_NUM="$2"


# Generate cumulated error log
./log_to_db.sh $BUILD_LOG $DB_NAME #new
cat $BUILD_LOG | $THIS/filter_errorlog.py $JOB $BUILD_NUM >>$ERROR_LOG #old

# now paint a graph from all builds recorded so far
cat $ERROR_LOG | \
    $THIS/to_json.py | \
    grep -P "(WARN_COUNT)|(ERR_COUNT)" | \
    $THIS/to_graph.py \
        "$GRAPH_FILE" \
        "$GRAPH_NAME" \
        "$LABEL_X" \
        "$LABEL_Y_LEFT" \
        "$LABEL_Y_RIGHT" \
        "$FORMAT_WARNINGS" \
        "$FORMAT_ERRORS"

# Finally collect compiler warnings of all components
echo -e "\n\n--------\n $JOB $BUILD_NUM\n----" >> $CC_WARNINGS_LOG
export overall=0 count=0
find "$THIS/../build/tmp-eglibc/work/" -name 'log.do_compile' | \
    { 
        while read file; do 
            num=$(grep -ci warning $file)
            if [ $num -gt 0 ] ; then 
                name=$(echo "$file" | sed -e 's/.*tmp-eglibc\/work\/[^/]*\/\([^/]*\)\/.*/\1/')
                printf "%10s warnings in %s\n" $num "$name" >>$CC_WARNINGS_LOG
                overall=$((overall + num))
                ((count ++))
            fi
          done; 
          echo -e "\n----\nCounted $overall warnings in $count packages\n--------" >> $CC_WARNINGS_LOG;
    }
