#!/bin/bash
echo "Create SFTP-Community in wangrob-sandbox-01."

aws cloudformation create-stack --stack-name sftp-community \
--template-body file://sftp-community.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://sftp-community-parameters.json \
--profile wangrob-sandbox-01 \
--region us-east-1

echo "Done"
