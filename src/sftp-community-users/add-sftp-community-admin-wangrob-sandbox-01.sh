#!/bin/bash
echo "Add SFTP-Community Admin=$1, Parameters File=$1.json in wangrob-sandbox-01."

aws cloudformation create-stack --stack-name sftp-community-admin-$1 \
--template-body file://sftp-community-admin.yaml \
--parameters file://$1.json \
--profile wangrob-sandbox-01 \
--region us-east-1

echo "Done"

