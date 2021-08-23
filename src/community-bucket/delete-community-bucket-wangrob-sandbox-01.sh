#!/bin/bash
echo "Delete community-bucket stack (including publishContent function) from wangrob-sandbox-01."

aws cloudformation delete-stack --stack-name community-bucket \
--profile wangrob-sandbox-01 \
--region us-east-1

echo "Done"
