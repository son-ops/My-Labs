#!/bin/sh
name=$(tr -dc 'a-zA-Z0-9' </dev/urandom | head -c 8)
echo 'SSS{test_flag}' > /${name}_flag.txt
exec python3 app.py ${name}_flag.txt