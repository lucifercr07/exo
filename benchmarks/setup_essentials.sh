#!/bin/bash

set -e
cd /home/ubuntu
sudo apt update && sudo apt install supervisor -y
sudo apt install python3.12 python3.12-venv -y

if [ ! -d "exo" ]; then
    git clone https://github.com/DiceDB/exo
    echo "Setup .env file in /home/ubuntu/exo directory"
    exit 1
else
    cd exo
    git pull origin master
fi

cd /home/ubuntu/exo

if [ ! -d "venv" ]; then
    python3.12 -m venv venv
fi

./venv/bin/pip install -r requirements.txt
