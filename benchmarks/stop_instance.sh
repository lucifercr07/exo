#!/bin/bash
set -e

echo "stopping the temporary instance:" $INSTANCE_ID
aws ec2 stop-instances --instance-ids $INSTANCE_ID > /dev/null
# X=$(aws ec2 terminate-instances \
#     --instance-ids $INSTANCE_ID \
#     --output json \
#     | jq -r '.TerminatingInstances[0].InstanceId')
