#!/bin/bash
echo "Add SFTP-Community Admin=$1, Parameters File=$1.json"

aws cloudformation create-stack --stack-name sftp-community-admin-$1 \
--template-body file://sftp-community-admin.yaml \
--parameters file://$1.json

echo "Done"

