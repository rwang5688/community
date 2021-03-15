#!/bin/bash
echo "Add SFTP-Community User=$1, Parameters File=$1.json"

aws cloudformation create-stack --stack-name sftp-community-user-$1 \
--template-body file://sftp-community-user.yaml \
--parameters file://$1.json

echo "Done"

