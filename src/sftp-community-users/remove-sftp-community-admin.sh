#!/bin/bash
echo "Remove SFTP-Community Admin $1"

aws cloudformation delete-stack --stack-name sftp-community-admin-$1 \
--profile wangrob-sandbox-01 \
--region us-east-1

echo "Done"

