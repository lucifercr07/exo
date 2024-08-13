#!/bin/bash

set -e

source setup_instance.sh
ssh -o StrictHostKeyChecking=no -i $SSH_PEM_PATH ubuntu@$INSTANCE_IP "sudo supervisorctl start mt1"
