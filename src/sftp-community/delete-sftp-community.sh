#!/bin/bash
echo "Delete SFTP-Community in default."

aws cloudformation delete-stack --stack-name sftp-community \
--profile default \
--region us-east-1

echo "Done"
