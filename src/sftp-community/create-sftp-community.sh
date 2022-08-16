#!/bin/bash
echo "Create SFTP-Community in default."

aws cloudformation create-stack --stack-name sftp-community \
--template-body file://sftp-community.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://sftp-community-parameters.json \
--profile default

echo "Done"
