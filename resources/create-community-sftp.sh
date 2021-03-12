#!/bin/bash
aws cloudformation create-stack --stack-name community-sftp \
--template-body file://sftp-server.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
ParameterKey=Vpc,ParameterValue=vpc-3540c55e \
ParameterKey=PublicSubnet1,ParameterValue=subnet-4256fb29 \
ParameterKey=PublicSubnet2,ParameterValue=subnet-d0a2b9aa \
ParameterKey=BucketStack,ParameterValue=community-bucket \
ParameterKey=CustomHostname,ParameterValue=sftp-community.octank.edu.rwang5688.com \
ParameterKey=HostedZone,ParameterValue=Z05028892SWHRH407JS0E
