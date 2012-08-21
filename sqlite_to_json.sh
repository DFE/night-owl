#!/bin/bash

#FIXME: This is all too much hackety hack. Rewrite!
json1="{"
json1="$json1 \"signal_tid\":\1,"
json1="$json1 \"type\":\"\2\","
json1="$json1 \"attempt\":\3,"
json1="$json1 \"msg\":\"\4\","
json1="$json1 \"cat\":\"\5\","
json1="$json1 \"recipe\":\"\6\","
json1="$json1 \"cmd\":\"\7\","
json1="$json1 \"file\":\"\8\","
#deadline hackety hack, because sed just allows until \9
json2="\1 \"row\":\2,"
json2="$json2 \"col\":\3,"
json2="$json2 \"time\":\"\4\""
json2="$json2 }"

e="\([^|]*\)"
sql="SELECT * FROM signal"

USAGE="usage: sqlite_to_json.sh <db_name>"

if [ -z $1 ]; then
    echo "$USAGE"
    exit 1
fi

sqlite3 $1 "$sql" | sed "s/\"/'/g" \
    | sed "s/$e|$e|$e|$e|$e|$e|$e|$e\(.*\)/$json1\9/" \
    | sed "s/$e|$e|$e|$e/$json2/" \
