#!/bin/bash
json="{'tid':\1,'type':\2,'msg':\3,'cat':\4}"
e="\([^|]*\)"
sql="SELECT * FROM signal"
sqlite3 dbmodell/test.db "$sql" | sed "s/$e|$e|$e|$e|$e|$e|$e|$e/$json/g"
