#!/bin/bash
set -e

sudo supervisorctl start redis
memtier_benchmark -s localhost -p 6379 -c 50 -t 10 \
    --key-pattern="R:R" --data-size=64 --ratio=1:1 --out-file=/home/ubuntu/mt1-redis.txt --hide-histogram
sudo supervisorctl stop redis

sleep 5

sudo supervisorctl start dicedb
memtier_benchmark -s localhost -p 7379 -c 50 -t 10 \
    --key-pattern="R:R" --data-size=64 --ratio=1:1 --out-file=/home/ubuntu/mt1-dicedb.txt --hide-histogram
sudo supervisorctl stop dicedb

cd /home/ubuntu/exo
./venv/bin/python ingest_mt_results.py manual redis 7.2.5 /home/ubuntu/mt1-redis.txt
./venv/bin/python ingest_mt_results.py manual dicedb 0.0.1 /home/ubuntu/mt1-dicedb.txt
