#!/bin/bash
aws cloudformation create-stack --stack-name community-bucket \
--region us-east-2 --template-body file://data-bucket.yaml \
--parameters \
ParameterKey=ProjectName,ParameterValue=community.octank.edu.rwang5688.com
