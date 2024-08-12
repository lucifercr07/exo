#!/bin/bash
set -e

cd /home/ubuntu
cd redis/src
nohup ./redis-server > /dev/null 2>&1 &

memtier_benchmark -s localhost -p 6379 -c 50 -t 10 \
    --key-pattern="R:R" --data-size=64 --ratio=1:1 --out-file=/home/ubuntu/mt1-redis.txt --hide-histogram

pkill -9 redis-server

cd /home/ubuntu
cd dice
nohup ./dice > /dev/null 2>&1 &

memtier_benchmark -s localhost -p 7379 -c 50 -t 10 \
    --key-pattern="R:R" --data-size=64 --ratio=1:1 --out-file=/home/ubuntu/mt1-dicedb.txt --hide-histogram

pkill -9 dice
