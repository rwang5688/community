#!/bin/bash
echo "Remove SFTP-Community User $1 from default."

aws cloudformation delete-stack --stack-name sftp-community-user-$1 \
--profile default

echo "Done"

