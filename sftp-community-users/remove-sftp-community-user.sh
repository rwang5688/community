#!/bin/bash
echo "Delete SFTP-Community User $1"

aws cloudformation delete-stack --stack-name sftp-community-user-$1

echo "Done"

