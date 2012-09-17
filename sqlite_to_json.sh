#!/bin/bash


sql="SELECT * FROM signal"

USAGE="usage: sqlite_to_json.sh <db_name>"

if [ -z $1 ]; then
    echo "$USAGE"
    exit 1
fi

sqlite3 $1 "$sql" | ./parse_sqlite.py
