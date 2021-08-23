#!/bin/bash
echo "Remove SFTP-Community Admin $1 from default."

aws cloudformation delete-stack --stack-name sftp-community-admin-$1 \
--profile default \
--region us-east-1

echo "Done"

