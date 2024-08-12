#!/bin/bash
set -e

cd /home/ubuntu

if [ ! -d "/usr/local/go" ]; then
    rm -rf go1.21.13.linux-amd64.tar.gz
    wget https://go.dev/dl/go1.21.13.linux-amd64.tar.gz
    sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.13.linux-amd64.tar.gz
fi

export PATH=$PATH:/usr/local/go/bin

if [ ! -d "dice" ]; then
    git clone https://github.com/dicedb/dice
fi

cd dice
/usr/local/go/bin/go build

cd /home/ubuntu
