#!/bin/bash
aws cloudformation update-stack --stack-name community-octank-edu-website-bucket \
--region us-east-2 --template-body file://community-octank-edu-website-bucket.yaml
