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

echo "[program:redis]
command=/home/ubuntu/redis/src/redis-server
autostart=false
autorestart=false
user=ubuntu
directory=/home/ubuntu/redis
stdout_logfile=/var/log/redis.log
stderr_logfile=/var/log/redis_error.log" | sudo tee /etc/supervisor/conf.d/redis.conf

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl stop redis
