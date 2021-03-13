#!/bin/bash
echo "Delete SFTP admin $1"

aws cloudformation delete-stack --stack-name community-sftp-admin-$1

echo "Done"

