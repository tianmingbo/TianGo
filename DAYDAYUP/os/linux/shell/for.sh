#!/bin/bash
for IP in $(cat tmp.txt); do
  ping -c 3 -i 0.2 -W 3 $IP &> /dev/null
  if [ $? -eq 0 ]; then
    echo "$IP online"
  else
    echo "$IP offLine"
  fi
done
