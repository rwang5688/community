#!/bin/bash
echo "Delete SFTP-Community in wangrob-sandbox-01."

aws cloudformation delete-stack --stack-name sftp-community \
--profile wangrob-sandbox-01 \
--region us-east-1

echo "Done"
