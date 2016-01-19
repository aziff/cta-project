#!/bin/bash
n=1
while [ $n -le 120 ]
do
echo "$n"
python2.7 scrape-api.py
n=$(( n+1 ))
sleep 30
done
