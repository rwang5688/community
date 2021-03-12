#!/bin/bash
aws cloudformation update-stack --stack-name community-octank-edu-website-bucket \
--template-body file://community-octank-edu-website-bucket.yaml --region us-east-2
