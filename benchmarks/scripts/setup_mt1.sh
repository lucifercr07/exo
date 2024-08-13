#!/bin/bash
set -e

cd /home/ubuntu

echo "[program:mt1]
command=/bin/bash /home/ubuntu/exo/benchmarks/scripts/mt1.sh
autostart=false
autorestart=false
user=ubuntu
directory=/home/ubuntu/redis
stdout_logfile=/var/log/mt1.log
stderr_logfile=/var/log/mt1.log" | sudo tee /etc/supervisor/conf.d/mt1.conf

sudo supervisorctl reread
sudo supervisorctl update
