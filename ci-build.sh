#!/bin/sh

PRE=nightowl
ERROR_LOG=$PRE-error.log
ERROR_GRAPH=$PRE-error

cat $1/log | ./filter_errorlog.py >>$ERROR_LOG
cat $ERROR_LOG | ./to_json.py | grep count | ./to_graph.py $ERROR_GRAPH
