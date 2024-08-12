#!/bin/bash
set -e

cd /home/ubuntu

if [ ! -d "redis" ]; then
    git clone https://github.com/redis/redis/
fi

cd redis
git checkout 7.2.5
make

cd /home/ubuntu
