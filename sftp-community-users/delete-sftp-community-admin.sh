#!/bin/bash
echo "Delete SFTP-Community Admin $1"

aws cloudformation delete-stack --stack-name sftp-community-admin-$1

echo "Done"

