#!/bin/bash
echo "Delete SFTP user $1"

aws cloudformation delete-stack --stack-name community-sftp-user-$1

echo "Done"

