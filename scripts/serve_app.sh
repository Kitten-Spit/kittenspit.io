#!/bin/bash


SERVER_DEFAULT='Waitress WSGI'


# make sure we exit flask as child process:
trap  "kill 0" EXIT


read -p "Serve with: [$SERVER_DEFAULT]: " SERVER
SERVER=${SERVER:-$SERVER_DEFAULT}
echo

wait

if [[ $SERVER  == $SERVER_DEFAULT ]]; then
  echo "Starting Flask via Waitress..."
  python3 application.py
  exit 0
else
  echo "Starting Flask via default WSGI..."
  flask run
  exit 0
fi
