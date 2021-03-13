#!/bin/bash
echo "Create SFTP User=$1, Parameters File=$1.json"

aws cloudformation create-stack --stack-name community-sftp-user-$1 \
--template-body file://sftp-server-user.yaml \
--parameters file://$1.json

echo "Done"

