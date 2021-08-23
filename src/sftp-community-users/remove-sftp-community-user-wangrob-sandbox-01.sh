#!/bin/bash
echo "Remove SFTP-Community User $1 from wangrob-sandbox-01."

aws cloudformation delete-stack --stack-name sftp-community-user-$1 \
--profile wangrob-sandbox-01 \
--region us-east-1

echo "Done"

