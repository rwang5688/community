#!/bin/bash
aws cloudformation create-stack --stack-name sftp-community-octank-edu-transfer-server \
--template-body file://sftp-community-octank-edu-transfer-server.yaml
