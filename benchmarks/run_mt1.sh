#!/bin/bash

set -e

source setup_instance.sh
echo "executing setup_redis.sh on $INSTANCE_IP"
ssh -o StrictHostKeyChecking=no -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP "/bin/bash /home/ubuntu/scripts/setup_redis.sh"
ssh -o StrictHostKeyChecking=no -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP "/bin/bash /home/ubuntu/scripts/setup_memtier.sh"
ssh -o StrictHostKeyChecking=no -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP "/bin/bash /home/ubuntu/scripts/mt1.sh"
scp -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP:/home/ubuntu/mt1-redis.txt ./results/mt1-redis.txt
ssh -o StrictHostKeyChecking=no -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP "/bin/bash /home/ubuntu/scripts/stop_redis.sh"
./venv/bin/python update_results.py results-memtier-1-redis.txt memtier-1-redis
bash stop_instance.sh
