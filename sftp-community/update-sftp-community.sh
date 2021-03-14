#!/bin/bash
aws cloudformation update-stack --stack-name sftp-community \
--template-body file://sftp-community.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://sftp-community-parameters.json
