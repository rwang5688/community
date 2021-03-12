#!/bin/bash
aws cloudformation create-stack --stack-name sftp-community-octank-edu-transfer-server \
--template-body file://sftp-community-octank-edu-transfer-server.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
ParameterKey=Vpc,ParameterValue=vpc-3540c55e \
ParameterKey=PublicSubnet1,ParameterValue=subnet-4256fb29 \
ParameterKey=PublicSubnet2,ParameterValue=subnet-d0a2b9aa \
ParameterKey=BucketStack,ParameterValue=community-octank-edu-website-bucket
