#!/bin/bash
read -p "请输入：" PRAM
case $PRAM in
[a-z] | [A-Z])
  echo "字母"
  ;;
[0-9])
  echo "数字"
  ;;
*)
  echo "other"
esac
