#!/bin/bash
PRICE=$(expr $RANDOM % 1000)
TIMES=0
echo "价格为0-999 $PRICE"
while true; do
  read -p "guess:" INT
  let TIMES++
  if [ "$INT" -eq "$PRICE" ]; then
    echo "答对了，用了$TIMES 次"
    exit 0
  elif [ "$INT" -gt "$PRICE" ]; then
    echo "太高了"
  else
    echo "太低了"
  fi
done
