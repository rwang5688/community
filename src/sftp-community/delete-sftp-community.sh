#!/bin/bash
aws cloudformation delete-stack --stack-name sftp-community \
--profile wangrob-sandbox-01 \
--region us-east-1
