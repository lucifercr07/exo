#!/bin/bash
set -e

cd /home/ubuntu

sudo apt-get update -y
sudo apt-get install -y build-essential autoconf automake libpcre3-dev \
    libevent-dev pkg-config zlib1g-dev libssl-dev

if [ ! -d "memtier_benchmark" ]; then
    git clone https://github.com/RedisLabs/memtier_benchmark
fi

cd memtier_benchmark

autoreconf -ivf
./configure
make
sudo make install
