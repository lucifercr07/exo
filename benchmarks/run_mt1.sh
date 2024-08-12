#!/bin/bash

set -e

source setup_instance.sh
echo "executing setup_redis.sh on $INSTANCE_IP"
ssh -o StrictHostKeyChecking=no -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP "/bin/bash /home/ubuntu/scripts/setup_memtier.sh"
ssh -o StrictHostKeyChecking=no -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP "/bin/bash /home/ubuntu/scripts/setup_redis.sh"
ssh -o StrictHostKeyChecking=no -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP "/bin/bash /home/ubuntu/scripts/setup_dicedb.sh"

ssh -o StrictHostKeyChecking=no -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP "/bin/bash /home/ubuntu/scripts/mt1.sh"
scp -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP:/home/ubuntu/mt1-redis.txt ./results/mt1-redis.txt
scp -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP:/home/ubuntu/mt1-dicedb.txt ./results/mt1-dicedb.txt

bash stop_instance.sh

cd ..
./venv/bin/python ingest_mt_results.py manual redis 7.2.5 ./benchmarks/results/mt1-redis.txt
./venv/bin/python ingest_mt_results.py manual dicedb 0.0.1 ./benchmarks/results/mt1-dicedb.txt
