#!/bin/bash
#test
DIR="/home/ubuntu/tianmingbo"
if [ ! -e $DIR ]
then
        mkdir - p $DIR
fi

#!/bin/bash
read -p "enter your score:" GRADE
if [ $GRADE -ge 85 ] && [ $GRADE -le 100 ];then
        echo "excellent"
elif [ $GRADE -ge 60 ] && [ $GRADE -lt 85 ];then
        echo "pass"
else
        echo "fial"
fi
