#!/bin/bash
echo "Create SFTP Admin=$1, Parameters File=$1.json"

aws cloudformation create-stack --stack-name community-sftp-admin-$1 \
--template-body file://sftp-server-admin.yaml \
--parameters file://$1.json

echo "Done"

