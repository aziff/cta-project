#!/bin/bash
n=1
while [ $n -le 657 ]
do
echo "$n"
python2.7 scrape_api.py
n=$(( n+1 ))
sleep 30
done
